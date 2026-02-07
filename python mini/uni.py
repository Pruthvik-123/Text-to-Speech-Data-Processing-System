from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import uuid
import speech_recognition as sr

app = Flask(__name__)

# Function to convert text to speech
def text_to_speech(text):
    unique_filename = f"static/speech_{uuid.uuid4().hex}.mp3"
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save(unique_filename)
    return unique_filename

# Function to recognize speech
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Timeout to prevent indefinite wait
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
        except sr.WaitTimeoutError:
            return "No speech detected, please try again."
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Error: Check network connection."

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tts', methods=['POST'])
def tts():
    text = request.form.get('text', '')
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400
    audio_path = text_to_speech(text)
    return jsonify({"audio": audio_path})

@app.route('/stt', methods=['GET'])
def stt():
    text = speech_to_text()
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Avoid debug mode interference
