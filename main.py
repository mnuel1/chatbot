from flask import Flask, request, jsonify
import json
from fuzzywuzzy import process
from qa import qa_data

app = Flask(__name__)


# Extract questions for fuzzy matching
questions = [item["question"] for item in qa_data]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("question")
    
    # Find best match
    best_match, confidence = process.extractOne(user_input, questions)
    
    # Set confidence threshold (adjust as needed)
    if confidence > 70:  # If the match is strong enough
        answer = next(item["answer"] for item in qa_data if item["question"] == best_match)
        return jsonify({"answer": answer})
    
    return jsonify({"answer": "I’m sorry, but I don’t have information on that."})  # No match found

if __name__ == "__main__":
    app.run(debug=True)
