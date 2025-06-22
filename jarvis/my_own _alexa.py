import google.generativeai as genai
import speech_recognition as sr
import pyttsx3, os, webbrowser
from datetime import datetime
genai.configure(api_key="your own api key")
model = genai.GenerativeModel("gemini-pro")

# Initialize speech recognizer & text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

response = model.generate_content("Hello,gemini")
print(response.text)

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
                    engine.say("Thank you")
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
            # Display recognized speech
            print(f"You said: {text}")
            # Speak out recognized text
            engine.say(text)
            engine.runAndWait()
            # return
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
        # elif "search" in text:
        #     search_query = text.replace("search", "").strip()  # Remove "search" from the query
        #     if search_query:
        #         search_url = f"https://www.google.com/search?q={search_query}"
        #         webbrowser.open(search_url)
        #         print(f"Searching for {search_query} on Google...")
        #         engine.say(f"Searching for {search_query} on Google")
        #         engine.runAndWait()
        elif "gemini" in text:
            search_query = text.replace("gemini", "").strip()  # Remove "search" from the query
            if search_query:
                search_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(search_url)
                print(f"Searching for {search_query} on Google...")
                engine.say(f"Searching for {search_query} on Google")
                engine.runAndWait()
        elif "youtube" in text:  
            print("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
            engine.say("Opening YouTube")
            engine.runAndWait()
        else:
            print("No search query detected.")

while True:
    hotword=listening_hotword()
    if hotword == "exit":
        print("Exiting program...")
        break  # Stop execution
    text=listening_command()
    executed_command(text)

