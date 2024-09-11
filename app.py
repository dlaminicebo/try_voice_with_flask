from flask import Flask, render_template, request, jsonify
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pyjokes
import webbrowser
import pywhatkit as kit
import os

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.8
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perform_task', methods=['POST'])
def perform_task():
    data = request.json
    command = data.get('command').lower()

    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        try:
            results = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            return jsonify({"response": results})
        except wikipedia.exceptions.DisambiguationError:
            return jsonify({"response": "There are multiple meanings. Please be more specific."})
        except wikipedia.exceptions.PageError:
            return jsonify({"response": "No Wikipedia page matches the query."})
    elif 'play' in command:
        song = command.replace('play', "")
        speak("Playing " + song)
        kit.playonyt(song)
        return jsonify({"response": f"Playing {song} on YouTube"})
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com/")
        return jsonify({"response": "Opening YouTube"})
    elif 'open google' in command:
        webbrowser.open("https://www.google.com/")
        return jsonify({"response": "Opening Google"})
    elif 'search' in command:
        search_query = command.replace('search', '')
        kit.search(search_query)
        return jsonify({"response": f"Searching for {search_query}"})
    elif 'the time' in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")
        return jsonify({"response": str_time})
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        return jsonify({"response": joke})
    else:
        return jsonify({"response": "Command not recognized"})

if __name__ == "__main__":
    app.run(debug=True)
