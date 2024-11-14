# views/chat_view.py
from flask import jsonify

def format_response(bot_response):
    return jsonify({"response": bot_response})
