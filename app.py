from flask import Flask, render_template, request, jsonify
import argostranslate.package
import argostranslate.translate

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
    "Chinese": "zh",
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
        return jsonify({"error": "Please enter text first."}), 400

    if source == target:
        return jsonify({"translation": text})

    try:
        # Make sure the requested language pair is installed.
        argostranslate.package.update_package_index()

        installed = argostranslate.translate.get_installed_languages()
        source_lang = next((x for x in installed if x.code == source), None)
        target_lang = next((x for x in installed if x.code == target), None)

        if not source_lang or not target_lang:
            raise Exception(f"Language not installed: {source}->{target}")

        translation = source_lang.get_translation(target_lang)
        translated = translation.translate(text)

        return jsonify({"translation": translated})

    except Exception as e:
        print("Translation error:", e)
        return jsonify({
            "error": f"Translation unavailable: {source} → {target}"
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
