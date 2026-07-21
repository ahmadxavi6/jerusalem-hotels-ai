import os
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    Response,
    stream_with_context,
)
from claude_client import ask_claude_stream, compare_hotels_stream
from rag import search_documents, search_documents_with_budget, detect_currency
from admin import admin_bp

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
app.register_blueprint(admin_bp, url_prefix="/admin")

conversations = {}


@app.route("/")
def home():
    return render_template("index.html")


import json


@app.route("/ask-stream", methods=["POST"])
def ask_stream():
    data = request.json
    question = data.get("question", "")
    session_id = data.get("session_id", "default")

    if session_id not in conversations:
        conversations[session_id] = []

    currency, rate = detect_currency(question, conversations[session_id])
    relevant_docs = search_documents_with_budget(question, conversations[session_id])

    full_response = []

    def generate():
        for chunk in ask_claude_stream(
            question, relevant_docs, conversations[session_id], currency, rate
        ):
            full_response.append(chunk)
            # Use JSON to safely encode the chunk
            yield f"data: {json.dumps(chunk)}\n\n"

        conversations[session_id].append({"role": "user", "content": question})
        conversations[session_id].append(
            {"role": "assistant", "content": "".join(full_response)}
        )
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route('/compare-stream', methods=['POST'])
def compare_stream():
    data = request.json
    hotel1 = data.get('hotel1', '')
    hotel2 = data.get('hotel2', '')

    docs1 = search_documents(hotel1)
    docs2 = search_documents(hotel2)
    all_docs = list(set(docs1 + docs2))

    full_response = []

    def generate():
        for chunk in compare_hotels_stream(hotel1, hotel2, all_docs):
            full_response.append(chunk)
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


if __name__ == '__main__':
    print("Starting server...")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
