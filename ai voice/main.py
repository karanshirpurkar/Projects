import speech_recognition as sr
import pyttsx3 as p
import wikipedia
import webbrowser

engine = p.init("sapi5")
voices = engine.getProperty("voices")
print(voices[1].id)
engine.setProperty("voice", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
    except Exception as e:
        print("say that again please....")
        return "none"
    return query

def search_google():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What do you want to search for on Google?")
        speak("What do you want to search for on Google?")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
        speak(f"Searching for {query} on Google.")
        query = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
    except Exception as e:
        print("Sorry, I didn't understand that.")
        speak("Sorry, I didn't understand that.")


def search_youtube():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What do you want to search for on YouTube?")
        speak("What do you want to search for on YouTube?")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
        speak(f"Searching for {query} on YouTube.")
        query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
    except Exception as e:
        print("Sorry, I didn't understand that.")
        speak("Sorry, I didn't understand that.")


if __name__ == "__main__":
    dictionary = {}
    while True:
        query = takecommand().lower()
        if 'wikipedia' in query:
            speak('searching wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            break
        elif 'search youtube' in query:
            search_youtube()
            break
        elif 'google' in query:
            search_google()
            break
        elif 'open instagram' in query:
            speak("opening instagram")
            webbrowser.open("instagram.com")
            break
        elif 'open whatsapp' in query:
            speak("opening whatsapp")
            webbrowser.open("web.whatsapp.com")
            break
        elif 'open facebook' in query:
            speak("opening facebook")
            webbrowser.open("facebook.com")
            break
        elif 'make a list' in query:
            list = []
            speak("what will be the name of list")
            name = takecommand().lower()
            i = 1
            while True:
                string = "element number {}".format(i)
                speak(string)
                print(string)
                element = takecommand().lower()
                if 'quit' in element:
                    break
                list.append(element)
                i += 1
            dictionary[name] = list
            speak(list)
        elif 'show me the list' in query:
            speak("which list")
            i = 1
            for x in dictionary.keys():
                speak(x)
                print("{}) {}".format(i, x))
            name_list = takecommand().lower()
            elements = str(dictionary[name_list])
            print(elements)
            speak(elements)
        elif 'keep quiet' in query or 'silence' in query or 'stop' in query:
            speak("Thanks for your time")
            break
