from flask import Flask, render_template, request, jsonify
from inference import Inference
from dotenv import load_dotenv
import os
from config import Config

load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not tavily_key or not groq_key:
    raise EnvironmentError("TAVILY_API_KEY and GROQ_API_KEY must be set in .env")

os.environ["TAVILY_API_KEY"] = tavily_key
os.environ["GROQ_API_KEY"] = groq_key 

app = Flask(__name__)
inference = None
config = Config()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    inference = Inference("Phebo from friends", config)
    #llm_response = inference.user_infer(user_message)
    llm_response = "test"
    return jsonify({
        'user_message': user_message,
        'llm_response': llm_response
    })

@app.route('/build', methods=['POST'])
def build():
    character = request.form['character']
    inference = Inference(character, config)

if __name__ == '__main__':
    app.run(debug=True)
