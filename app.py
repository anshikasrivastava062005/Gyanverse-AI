from flask import Flask, render_template, request, jsonify
from utils import ask_ai
from scanner import extract_text
from embedding_rag import save_notes, get_context

app = Flask(__name__)

latest_text = ""

@app.route("/")
def home():
    return render_template("index.html")


#  ASK AI 
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")

    context = get_context(user_question)
    print("CONTEXT:", context)

    prompt = f"""
    You are a helpful AI tutor.
    
    Answer ONLY using the provided context.
    Explain clearly in simple words.
    
    If answer is not found, say: "Not found in notes."
    
    Context:
    {context}
    
    Question:
    {user_question}
    """

    response = ask_ai(prompt)

    return jsonify({"answer": response})


#  OCR UPLOAD 
@app.route("/upload", methods=["POST"])
def upload():
    global latest_text

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filepath = "temp.png"
    file.save(filepath)

    #  FIXED FUNCTION CALL
    text = extract_text(filepath)

    print("EXTRACTED TEXT:", text)

    if not text.strip():
        return jsonify({"text": "No text detected", "topic": ""})

    save_notes(text)

    latest_text = text

    return jsonify({
        "text": text
    })


#  MCQ GENERATION
@app.route("/generate_mcq", methods=["GET"])
def generate_mcq():
    global latest_text

    if not latest_text:
        return jsonify({"mcq": "Upload notes first 📄"})

    prompt = f"""
    Based ONLY on the following notes:

    {latest_text}

    Generate 5 MCQs.
    Format:
    Q1:
    A)
    B)
    C)
    D)
    Answer:
    """

    response = ask_ai(prompt)

    return jsonify({"mcq": response})


if __name__ == "__main__":
    app.run(debug=True)