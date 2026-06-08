from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import time
import uuid
from gtts import gTTS
import os
languages = GoogleTranslator().get_supported_languages(as_dict=True)
from indic_transliteration.sanscript import (
    transliterate,
    TELUGU,
    DEVANAGARI
)

app = Flask(__name__)


def is_telugu_script(text):

    for char in text:

        if '\u0C00' <= char <= '\u0C7F':
            return True

    return False


@app.route("/", methods=["GET", "POST"])
def home():

    translated_text = ""
    transliterated_text = ""
    detected_language = ""
    audio_file = None

    if request.method == "POST":

        text = request.form["text"]

        source_lang = request.form["source_language"]

        target_lang = request.form["target_language"]

        lyrics_mode = request.form.get("lyrics_mode")

        if lyrics_mode and is_telugu_script(text):

            detected_language = "Hindi written in Telugu script"

            transliterated_text = transliterate(
                text,
                TELUGU,
                DEVANAGARI
            )

            translated_text = GoogleTranslator(
                source="hi",
                target=target_lang
            ).translate(transliterated_text)

        else:

            translated_text = GoogleTranslator(
                source=source_lang,
                target=target_lang
            ).translate(text)

        if translated_text:

            language_map = {
                "en": "en",
                "hi": "hi",
                "te": "te",
                "fr": "fr",
                "de": "de",
                "es": "es"
            }

            tts_lang = language_map.get(
                target_lang,
                "en"
            )

            try:

                tts = gTTS(text=translated_text, lang=tts_lang)

                filename = f"audio_{uuid.uuid4().hex}.mp3"
                audio_path = os.path.join("static", filename)

                tts.save(audio_path)

                audio_file = filename

            except Exception as e:

                print("TTS Error:", e)

    return render_template(
        "index.html",
        translated_text=translated_text,
        transliterated_text=transliterated_text,
        detected_language=detected_language,
        audio_file=audio_file,
        languages=languages
    )


if __name__ == "__main__":

    app.run(debug=True)