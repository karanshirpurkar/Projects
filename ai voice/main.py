import speech_recognition as sr
import pyttsx3 as p
import wikipedia
import webbrowser

engine=p.init("sapi5")
voices=engine.getProperty("voices")
print(voices[1].id)
engine.setProperty("voice",voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.pause_threshold=1
        audio = r.listen(source)

    try:
        print("recognising...")
        query=r.recognize_google(audio,language='en-in')
        print(f'User said: {query}\n')
    except Exception as e:
        print("say that again please....")
        return "none"
    return query


if __name__=="__main__":
    dictionary={}
    while True:
        query=takecommand().lower()
        if 'wikipedia' in query:
            speak('searching wikipedia....')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            break
        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
            break

        elif 'open google' in query:
            speak("opening Google")
            webbrowser.open("google.com")
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
            speak("opening facebool")
            webbrowser.open("facebook.com")
            break



            speak("Thanks for your time")
            break

        elif "make a list" in query:
            list=[]
            speak("what will be the name of list")
            name=takecommand().lower()
            i=1
            while True:
                string="element number {}".format(i)
                speak(string)
                print(string)
                element=takecommand().lower()
                if 'quit' in element:
                    break
                list.append(element)
                i+=1

            dictionary[name]=list
            speak(list)

        elif "show me the list" in query:
            speak("which list")
            i=1
            for x in dictionary.keys():
                speak(x)
                print("{}) {}".format(i,x))
            name_list=takecommand().lower()
            elements=str(dictionary[name_list])
            print(elements)
            speak(elements)
            """speak("Do You want to edit this list. Please answer yes or no")
            decision=takecommand().lower()
            if "no" in decision:
                break
            else:
                speak(" What you want to do Insert an element or delete or replace an element")
                command=takecommand().lower()
                if "insert" in command:
                    speak("What you want to insert")
                    new_element=takecommand().lower()
                    dictionary[name_list].append(new_element)
                elif "delete" in command:
                    delete_element=takecommand().lower()
                    dictionary[name_list].remove(delete_element)
            break"""

        elif "keep quite" or "silence" or "stop" in query:
            speak("Thanks for your time")
            break








