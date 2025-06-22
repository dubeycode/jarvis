import google.generativeai as genai
import speech_recognition as sr
import pyttsx3, os, webbrowser
from datetime import datetime

# Initialize speech recognizer & text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()
genai.configure(api_key=" llm api key ")
model = genai.GenerativeModel("gemini-pro")

def listening_hotword():
    print("Waiting for hotword...")
    while True:
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Capture the audio
                audio_text = r.listen(source)
                # Convert speech to text
                text = r.recognize_google(audio_text, language="en-in").lower()  # Convert to lowercase
                if text=="hey alexa":
                    engine.say("Yes i am listening")
                    engine.runAndWait()
                    return text
                elif text=="ok alexa bye":
                    engine.say("Thank you for using me Buy a cup of tea for me ")
                    engine.runAndWait()
                    return "exit"
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error. Please check your connection.")
            except Exception as e:
                print(f"Error: {str(e)}")  # Other unexpected errors
                text = ""


#---------------------------------- Lestening Commands--------------------------#
def listening_command():
    # Process commands only if text is recognized
    with sr.Microphone() as source:
        print("Listening... Speak now!")

        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Capture the audio
            audio_text = r.listen(source)
            # Convert speech to text
            text = r.recognize_google(audio_text, language="en-in").lower()  # Convert to lowercase
            print(f"You said: {text}")
            # Speak out recognized text
            engine.say(text)
            engine.runAndWait()
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")  # When speech is unclear
            text = ""  # Set text to empty string to prevent errors
        except sr.RequestError:
            print("Network error. Please check your connection.")  # When Google API fails
            text = ""
        except Exception as e:
            print(f"Error: {str(e)}")  # Other unexpected errors
            text = ""
#---------------------------------- Executed command --------------------------#
def executed_command(text):
    if text:
        if "notepad" in text:
            os.system("notepad")
        elif "chrome" in text:
            os.system("start chrome")  # Works for Windows

        elif "time" in text:
            current_time = datetime.now().strftime("%H:%M")
            print(f"The time is {current_time}")
            engine.say(f"The time is {current_time}")
            engine.runAndWait()
        
        elif "youtube" in text:  
            print("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
            engine.say("Opening YouTube")
            engine.runAndWait()
        else:
            response = model.generate_content(f"{text}")
            Answer=(response.text)
            engine.say(Answer)
            # Speak out recognized text
            engine.runAndWait()
while True:
    hotword=listening_hotword()
    if hotword == "exit":
        print("Exiting program...")
        break  # Stop execution
    text=listening_command()
    executed_command(text)

