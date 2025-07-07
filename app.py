from flask import Flask, request, jsonify
from chatbot import get_response, knowledge_base
from flask_cors import CORS
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response = get_response(user_input, knowledge_base)
    return jsonify({'response': response})
    #return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)


