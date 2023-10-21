from flask import Flask, render_template, request, jsonify
from chat import handle_message

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    message = request.form['message']
    # On message input, get response from chatbot
    response = handle_message(message)
    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=True)
