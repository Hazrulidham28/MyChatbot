# app.py
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# Load environment variables
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")

app = Flask(__name__)


client = OpenAI(
    api_key=RUNPOD_API_KEY,
    base_url=f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/openai/v1",
)

def generate_response(query):
    # Combine context and query for better response generation
    prompt = query
    response = client.chat.completions.create(
        model = "TechxGenus/Meta-Llama-3-8B-Instruct-AWQ",
        messages=[
        {"role": "system", "content": "You are help full AI assistance that will answer everything about Malaysian or its culture. If the question ask anything else, do not answer"},
        {
            "role": "user",
            "content":prompt,
        },
    ],
    temperature=0.7,
    max_tokens=512,
    )

    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.form['query']
    response = generate_response(user_query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
