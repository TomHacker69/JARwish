import speech_recognition as sr   # to recognition of the voice 
import pyttsx3   # for text to speech 
import webbrowser  # to open and website , whose url is given
import requests  # for API requests
from openai import OpenAI
from gtts import gTTS
import os
import pygame

recognizer = sr.Recognizer()  #function to recongnise the voice
engine = pyttsx3.init() #function to convert the voice into text
newsapi = "pub_2a0b10d988a8447fa4388794f17f3fe2"
openai_api_key = "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"

def speak_old(text):  # initializing the voice and text function
    engine.say(text)
    engine.runAndWait()
 
def speak(text): # using gtts for text to speech conversion
    try:
        tts = gTTS(text=text, lang='en')
        tts.save('temp.mp3')
        # Initializing pygame mixer
        pygame.mixer.init()
        # Load and play the mp3 file
        pygame.mixer.music.load('temp.mp3')
        # Play the audio
        pygame.mixer.music.play()
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if os.path.exists('temp.mp3'):
            os.remove('temp.mp3')  # Remove the temporary file after playing
    
    
def aiprocess(command):
    try:
        client = OpenAI(
            api_key=openai_api_key
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general task like Alexa and goggle Cloud and try to answer the question in only few lines"},
                {"role": "user", "content": command}
            ]
        )  
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI service error: {e}"  
    
if __name__ == "__main__":
    speak("Initializing voice assistant, command mode activated.")   # innitializing the voice assistant 
    
    # listen for the word "Tomhacker"
    # then listen for the command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for the wake word...")  # microphone in use and listen for the wakeup word
        audio = r.listen(source)
        
        try:   # using the (TRY - IF- ELIF ) to categeroise different types of the commands
            wake_word = r.recognize_google(audio)   # using the goggle voice recognition function
            if "Jarvis" in wake_word:   # if got  the  wakeword = "Tomhacker"
                speak("How can I assist you?")
                print("Listening for command...")
                audio = r.listen(source)   # to fasten the input and output functions
                command = r.recognize_google(audio)
                print(f"Command received: {command}")
                # different command that you can can use for the voice assistant , to give the output
                if "open YouTube" in command:
                    webbrowser.open("https://www.youtube.com")
                    speak("Opening YouTube")
                elif "open Google" in command:
                    webbrowser.open("https://www.google.com")
                    speak("Opening Google")
                elif command.lower().startswith("play"):
                    song_name = command.lower().split(" ")[1]
                    search_url = f"https://www.youtube.com/results?search_query={song_name}"
                    webbrowser.open(search_url)
                    speak(f"Searching for {song_name} on YouTube")
                elif "news" in command:
                    try:
                        response = requests.get("https://newsdata.io/api/1/latest?apikey=pub_2a0b10d988a8447fa4388794f17f3fe2&q=cyber%20security")
                        data = response.json()
                        if data.get("status") == "success":
                            articles = data.get("results", [])
                            print(f"Found {len(articles)} articles about cyber security:\n")
                            speak(f"Found {len(articles)} cyber security news articles")
                            
                            for i, article in enumerate(articles[:3]):  # Show only first 3
                                title = article.get("title", "No title")
                                link = article.get("link", "No URL")
                                pub_date = article.get("pubDate", "No date")

                                print(f"Title: {title}")
                                print(f"Published: {pub_date}")
                                print(f"Link: {link}")
                                print("-" * 60)
                        else:
                            print("Error fetching news data")
                            speak("Sorry, I couldn't fetch the news")
                
                    except Exception as e:
                        print(f"News API error: {e}")
                        speak("Sorry, there was an error getting the news")
                else: #let open ai will handel the rest of the commands , integrating OPEN AI - api keys
                    try:
                        response = aiprocess(command)
                        print(f"AI Response: {response}")
                        speak(response)
                    except Exception as e:
                        print(f"AI Error: {e}")
                        speak("Sorry, AI service is unavailable")
                
            else:   # if no command is receved within 2 min of  duration
                print("Wake word not detected.")
        

        except sr.UnknownValueError:  # if the voice assistant is not able to recognise the audio
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:  
            print(f"Could not request results; {e}")




# we can also add gtts for the text to speech funcnality and also news api for getting the latest news