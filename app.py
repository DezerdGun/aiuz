# app.py
from flask import Flask
from controllers.chat_controller import handle_chat_request, handle_settings_request

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    return handle_chat_request()

@app.route('/settings', methods=['POST'])
def settings():
    return handle_settings_request()

if __name__ == '__main__':
    app.run(debug=True)
