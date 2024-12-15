# app.py
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# Load environment variables
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")
HF_ENDPOINT_ID =  os.getenv("HF_ENDPOINT_ID")
GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")

app = Flask(__name__)


runpod_client = OpenAI(
    api_key=RUNPOD_API_KEY,
    base_url=f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/openai/v1",
)

gemma_client = OpenAI(
	base_url=HF_ENDPOINT_ID,
	api_key=GEMMA_API_KEY
)

def generate_response_runPod(query):
    # Combine context and query for better response generation
    prompt = query
    response = runpod_client.chat.completions.create(
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

def generate_response_gemma(query):
    # Combine context and query for better response generation
    prompt = f"""
    You are a helpfull AI assistance that will help user answer question related to Malaysian. If user ask other than that, do not answer.
    You also need to return the answer with the html tag, such as including the line break and etc...

    query: {query}
    """
    response = gemma_client.chat.completions.create(
        model = "google/gemma-2-27b-it",
        messages=[
        {
            "role": "user",
            "content":prompt,
        },
    ],
    temperature=0.7,
    max_tokens=1512,
    )

    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.form['query']
    response = generate_response_gemma(user_query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)


# venv\Scripts\activate