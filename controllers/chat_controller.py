# controllers/chat_controller.py
from flask import request, jsonify
from models.chat_model import ChatModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Инициализация модели
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Инициализация модели для хранения истории чатов и настроек
chat_model = ChatModel()

def generate_response(user_input, user_id):
    try:
        chat_history_ids = chat_model.get_chat_history(user_id)
        style = chat_model.get_user_settings(user_id)['style']

        if style == 'formal':
            user_input = f"Уважаемый пользователь, {user_input}"
        elif style == 'casual':
            user_input = f"Эй, дружище, {user_input}"

        # Токенизация ввода
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)

        if chat_history_ids is not None:
            input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        else:
            input_ids = new_user_input_ids

        # Генерация ответа
        chat_history_ids = model.generate(
            input_ids,
            max_length=150,
            min_length=20,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            temperature=0.6,
            top_k=50,
            top_p=0.9,
        )

        # Декодируем и возвращаем ответ
        bot_response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

        # Сохраняем обновленную историю чатов
        chat_model.set_chat_history(user_id, chat_history_ids)

        return bot_response if bot_response.strip() else "Извините, я не могу понять ваш запрос."
    
    except Exception as e:
        print(f"Error: {e}")
        return "Произошла ошибка при обработке запроса."

def handle_chat_request():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    user_id = data.get('user_id', 'default_user')

    if not user_message:
        return jsonify({"response": "Ошибка: Пожалуйста, введите сообщение."}), 400

    # Генерация ответа
    bot_response = generate_response(user_message, user_id)

    return jsonify({"response": bot_response})

def handle_settings_request():
    data = request.get_json()
    user_id = data.get('user_id')
    style = data.get('style')

    if not user_id or not style:
        return jsonify({"response": "Ошибка: Пожалуйста, укажите user_id и стиль."}), 400

    if style not in ["normal", "formal", "casual"]:
        return jsonify({"response": "Ошибка: Стиль может быть 'normal', 'formal' или 'casual'."}), 400

    # Обновляем настройки
    chat_model.set_user_settings(user_id, style)
    return jsonify({"response": f"Стиль общения для пользователя {user_id} обновлен на {style}."})
