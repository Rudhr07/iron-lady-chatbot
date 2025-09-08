from flask import Flask, render_template, request, Response
import requests
import json

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

IRON_LADY_CONTEXT = """
You are IRON LADY's official chatbot. Only answer questions related to IRON LADY and its programs.
If the user asks something unrelated, reply politely: 
"I'm here to help you with IRON LADY related queries only."

IRON LADY Information:
- Leadership development programs designed for women professionals and leaders.
- Program Duration: A few weeks to a few months, depending on the course.
- Mode: Primarily online, with some offline workshops.
- Certificates: Provided after successful completion.
- Mentors: Experienced coaches, industry experts, and senior leaders.

Keep answers short, clear, and professional.
"""

def stream_ollama(prompt):
    payload = {
        "model": "llama3",
        "prompt": f"{IRON_LADY_CONTEXT}\nUser: {prompt}\nBot:",
        "stream": True,
        "options": {
            "num_predict": 80,
            "temperature": 0.5
        }
    }
    with requests.post(OLLAMA_API_URL, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    yield data["response"]

@app.route("/", methods=["GET"])
def home():
    return render_template("landing.html")

@app.route("/chatbot", methods=["GET"])
def chatbot_only():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    return Response(stream_ollama(user_input), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
