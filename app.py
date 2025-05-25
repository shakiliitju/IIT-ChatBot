from flask import Flask, request, jsonify
from multi_website_knowledge_chatbot import get_response, knowledge_base
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response = get_response(user_input, knowledge_base)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)


