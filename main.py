import speech_recognition as sr

import pyttsx3

import wikipedia

from googlesearch import search

from transformers import AutoModelForCausalLM, AutoTokenizer

import torch

import webbrowser

import openai

openai.api_key = "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"

✅ Speak function with audio guarantee

def speak(text):

print("Assistant:", text)

engine = pyttsx3.init('sapi5')  # Ensure TTS engine works

engine.setProperty("rate", 150)

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)  # Change to voices[1] for female

engine.say(text)

engine.runAndWait()

✅ Listen from mic

def listen():

r = sr.Recognizer()

with sr.Microphone() as source:

    r.adjust_for_ambient_noise(source, duration=1)

    print("🎤 Speak now...")

    audio = r.listen(source)

try:

    print("🎧 Recognizing...")

    query = r.recognize_google(audio)

    print("You said:", query)

    return query

except:

    speak("Sorry, I couldn't understand.")

    return ""

✅ Wikipedia search

def get_wikipedia_answer(query):

try:

    return wikipedia.summary(query, sentences=2)

except:

    return None

✅ Google search result

def get_google_result(query):

try:

    for result in search(query, num_results=1):

        return f"Here is a result from Google: {result}"

except:

    return None

✅ AI fallback answer

def get_ai_response(query):

try:

    input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors='pt')

    chat_history_ids = model.generate(

        input_ids,

        max_length=1000,

        pad_token_id=tokenizer.eos_token_id,

        do_sample=True,

        top_p=0.95,

        top_k=50

    )

    reply = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    return reply

except:

    return "Sorry, I couldn't answer that."

✅ Load model

speak("Loading AI model. Please wait...")

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

✅ Initial greeting

speak("Hello! I am your smart voice assistant. If you need anything, just say vishal.")

✅ Wake loop

while True:

print("⏳ Waiting for 'vishal'...")

trigger = listen().lower()

if "vishal" in trigger:

    speak("Ya?")



    # Listen for actual command

    query = listen().lower()

    if not query:

        continue



    # ✅ Exit command

    if any(x in query for x in ["exit", "quit", "close", "stop"]):

        speak("Goodbye! Have a great day.")

        break



    # ✅ Open common websites

    elif "open google" in query:

        webbrowser.open("https://google.com")

        speak("Opening Google.")

        continue

    elif "open facebook" in query:

        webbrowser.open("https://facebook.com")

        speak("Opening Facebook.")

        continue

    elif "open youtube" in query:

        webbrowser.open("https://youtube.com")

        speak("Opening YouTube.")

        continue

    elif "open linkedin" in query:

        webbrowser.open("https://linkedin.com")

        speak("Opening LinkedIn.")

        continue



    # ✅ Wikipedia

    answer = get_wikipedia_answer(query)

    if answer:

        speak(answer)

        continue



    # ✅ Google search

    answer = get_google_result(query)

    if answer:

        speak(answer)

        continue



    # ✅ AI fallback

    answer = get_ai_response(query)

    if answer:

        speak(answer)

    else:

        speak("Sorry, I couldn't find anything useful.")