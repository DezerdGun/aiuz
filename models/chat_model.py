# models/chat_model.py
class ChatModel:
    def __init__(self):
        # История чатов пользователей
        self.user_chat_history = {}
        # Настройки пользователей
        self.user_settings = {}

    def get_chat_history(self, user_id):
        return self.user_chat_history.get(user_id, None)

    def set_chat_history(self, user_id, chat_history_ids):
        self.user_chat_history[user_id] = chat_history_ids

    def get_user_settings(self, user_id):
        return self.user_settings.get(user_id, {'style': 'normal'})

    def set_user_settings(self, user_id, style):
        self.user_settings[user_id] = {'style': style}
