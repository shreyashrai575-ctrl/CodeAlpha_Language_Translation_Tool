from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa"
}


@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}

    text = (data.get("text") or "").strip()
    source = data.get("source", "en")
    target = data.get("target", "hi")

    if not text:
        return jsonify({"error": "Please enter some text."}), 400

    try:
        url = "https://api.mymemory.translated.net/get"

        response = requests.get(
            url,
            params={
                "q": text,
                "langpair": f"{source}|{target}"
            },
            timeout=15
        )

        response.raise_for_status()
        result = response.json()

        translated = result.get("responseData", {}).get("translatedText")

        if not translated:
            raise Exception("No translation returned")

        return jsonify({"translation": translated})

    except Exception as e:
        print("Translation error:", e)

        return jsonify({
            "error": "Translation failed. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
