from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es"
}

# Free public LibreTranslate mirror
TRANSLATION_API = "https://translate.flossboxin.org.in/translate"


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

    if source not in LANGUAGES.values():
        return jsonify({
            "error": "Unsupported source language."
        }), 400

    if target not in LANGUAGES.values():
        return jsonify({
            "error": "Unsupported target language."
        }), 400

    if source == target:
        return jsonify({
            "translation": text
        })

    try:
        response = requests.post(
            TRANSLATION_API,
            json={
                "q": text,
                "source": source,
                "target": target,
                "format": "text"
            },
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )

        print("Translation server status:", response.status_code)
        print("Translation server response:", response.text[:500])

        response.raise_for_status()

        result = response.json()

        translated = result.get("translatedText")

        if not translated:
            return jsonify({
                "error": "Translation service returned no translation."
            }), 502

        return jsonify({
            "translation": translated
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Translation service timed out. Please try again."
        }), 504

    except requests.exceptions.RequestException as e:
        print("Translation request error:", repr(e))

        return jsonify({
            "error": "Translation service is temporarily unavailable."
        }), 502

    except ValueError:
        return jsonify({
            "error": "Translation service returned an invalid response."
        }), 502

    except Exception as e:
        print("Unexpected translation error:", repr(e))

        return jsonify({
            "error": "Translation failed. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
