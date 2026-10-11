import speech_recognition as sr
import csv
from difflib import get_close_matches
import os
r = sr.Recognizer()

def listen_once():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("speak now.....")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def saved_names():
    names = set()
    if not os.path.exists("sales.csv"):
        return []
    with open("sales.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.add(row["customer"].lower().strip())
    return list(names)
    
def get_name():
    heard = listen_once()
    names=saved_names()
    if heard != "":
        print("Heard:", heard)
        answer = input("Correct? (y/n): ").lower().strip()

        if answer == "y" and heard.lower().strip() in names:
            name = heard
        else:
            matches = get_close_matches(heard.lower().strip(), names, n=1, cutoff=0.5)
            if matches:
                print("Did you mean", matches[0], "?")
                answer2 = input("(y/n): ").lower().strip()
                if answer2 == "y":
                    name = matches[0]
                else:
                    name = input("type the name: ")
            else:
                name = input("type the name: ")
    else:
        print("Could not hear. Please type.")
        name = input("type the name: ")
    name = name.lower().strip()
    return name
print("Final name:", get_name())
