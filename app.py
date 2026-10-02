from flask import Flask, render_template, request, jsonify
from deep_translator import MyMemoryTranslator

app = Flask(__name__)

LANGUAGES = {
    "English": "english",
    "Hindi": "hindi",
    "French": "french",
    "Spanish": "spanish",
    "German": "german",
    "Italian": "italian",
    "Portuguese": "portuguese",
    "Japanese": "japanese",
    "Korean": "korean",
    "Chinese": "chinese simplified",
    "Arabic": "arabic",
    "Russian": "russian",
    "Bengali": "bengali",
    "Tamil": "tamil india",
    "Telugu": "telugu",
    "Marathi": "marathi",
    "Gujarati": "gujarati",
    "Punjabi": "punjabi",
}


@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}

    text = (data.get("text") or "").strip()
    source = data.get("source", "english")
    target = data.get("target", "hindi")

    if not text:
        return jsonify({"error": "Please enter some text."}), 400

    if target not in LANGUAGES.values():
        return jsonify({"error": "Unsupported target language."}), 400

    try:
        translator = MyMemoryTranslator(
            source=source,
            target=target
        )

        translated = translator.translate(text)

        return jsonify({
            "translation": translated
        })

    except Exception as e:
        print("Translation error:", e)

        return jsonify({
            "error": "Translation failed. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
