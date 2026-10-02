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


def install_language_pair(source, target):
    """Install an Argos language pair if it is not already installed."""

    if source == target:
        return True

    installed_packages = argostranslate.package.get_installed_packages()

    already_installed = any(
        package.from_code == source and package.to_code == target
        for package in installed_packages
    )

    if already_installed:
        return True

    print(f"Installing translation package: {source} -> {target}")

    argostranslate.package.update_package_index()

    success = argostranslate.package.install_package_for_language_pair(
        source,
        target
    )

    return success


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
        return jsonify({
            "error": "Please enter text first."
        }), 400

    if source not in LANGUAGES.values() or target not in LANGUAGES.values():
        return jsonify({
            "error": "Unsupported language."
        }), 400

    if source == target:
        return jsonify({
            "translation": text
        })

    try:
        # Install the required model if necessary.
        if not install_language_pair(source, target):
            return jsonify({
                "error": f"Translation model unavailable for {source} → {target}."
            }), 502

        # Perform the translation locally.
        translated = argostranslate.translate.translate(
            text,
            source,
            target
        )

        return jsonify({
            "translation": translated
        })

    except Exception as e:
        print("Translation error:", e)

        return jsonify({
            "error": "Translation failed. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
