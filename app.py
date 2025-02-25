import torch
from transformers import T5ForConditionalGeneration, RobertaTokenizer
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Load fine-tuned CodeT5 model and tokenizer
MODEL_PATH = "./codeT5-flutter"
tokenizer = RobertaTokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route("/autocomplete", methods=["POST"])
def autocomplete():
    try:
        data = request.get_json(force=True)  # 👈 Ensure JSON parsing
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    input_text = data["code"].strip()
    print(input_text)

    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    # Generate completion
    outputs = model.generate(**inputs, max_length=50, num_return_sequences=3, temperature=0.7, num_beams=5, do_sample = True)

    # Decode predictions
    suggestions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    print(suggestions)
    print(jsonify({"suggestions": suggestions}))
    return jsonify({"suggestions": suggestions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
