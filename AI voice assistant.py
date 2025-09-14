import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import pyjokes
import time
import warnings
import logging

# Suppress pyttsx3 + comtypes warnings
warnings.filterwarnings("ignore", category=UserWarning, module='comtypes')
logging.getLogger('comtypes').setLevel(logging.CRITICAL)

# Set your name here
user_name = "Suha"

# Initialize recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  #voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wait_for_continue():
    """Wait until user says 'continue' to resume the assistant."""
    speak("Say 'continue' when you're ready for the next command.")
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Waiting for 'continue'...")
                audio = r.listen(source)
                command = r.recognize_google(audio).lower()
                print("You said (in wait):", command)  # Debug output
                if 'continue' in command:
                    break
                else:
                    speak("Please say 'continue' to resume.")
        except Exception as e:
            print("Error in wait_for_continue():", e)
            speak("Sorry, I didn’t catch that. Say 'continue' when you're ready.")

def commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Listening...')
            audio = r.listen(source)

        try:
            my_text = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return True
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return True

        my_text = my_text.lower()
        print("You said:", my_text)

        if 'play' in my_text:
            song = my_text.replace('play', '')
            speak('Playing ' + song)
            pywhatkit.playonyt(song)
            wait_for_continue()

        elif 'date' in my_text:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak("Today's date is " + today)

        elif 'time' in my_text:
            timenow = datetime.datetime.now().strftime('%I:%M %p')
            speak("The time is " + timenow)

        elif 'who is' in my_text:
            person = my_text.replace('who is', '')
            try:
                info = wikipedia.summary(person, sentences=1)
                speak(info)
            except:
                speak("Sorry, I couldn't find information about " + person)

        elif 'say a joke' in my_text:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'exit' in my_text or 'stop' in my_text:
            speak(f"Goodbye, {user_name}. Shutting down.")
            return False

        else:
            speak("Sorry, I don't understand that command.")

    except Exception as e:
        print('Microphone error:', str(e))
        speak("There was a problem with the microphone.")
    return True

def run_assistant():
    speak(f"Hello {user_name}, what can I do for you?")
    while True:
        if not commands():
            break
        time.sleep(1)

if __name__ == "__main__":
    run_assistant()
