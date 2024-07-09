import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import json
import pickle
import json
import pickle
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cv2
import random
import numpy as np
import psutil
import subprocess

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)


def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    rate = engine.getProperty("rate")
    engine.setProperty("rate", rate - 50)
    volume = engine.getProperty("volume")
    engine.setProperty("volume", volume + 0.25)
    return engine


def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.....", end="", flush=True)
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment = 2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing....", end="", flush=True)
        query = r.recognize_google(audio, language="en-in")
        print("\r", end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("say that again please")
        return "None"
    return query


def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week


def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if (hour >= 0) and (hour <= 12) and ("AM" in t):
        speak(f"Good morning Bhavesh, it's {day} and the time is {t}")

    elif (hour >= 12) and (hour <= 16) and ("PM" in t):
        speak(f"Good afternoon Bhavesh, it's {day} and the time is {t}")

    elif (hour >= 16) and (hour <= 18) and ("PM" in t):
        speak(f"Good evening Bhavesh, it's {day} and the time is {t}")
    else:
        speak(f"Good night Bhavesh, it's {day} and the time is {t}")


def social_media(command):
    if "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "discord" in command:
        speak("Opening Discord server")
        webbrowser.open("https://discord.com")

    elif "twitter" in command:
        speak("Opening Twitter")
        webbrowser.open("https://www.twitter.com")

    elif "linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "Gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")

    elif "youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")

    else:
        speak("Sorry, I can't perform that action at the moment. Please try again.")


def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is")
    week = {
        "monday": "Boss, 6:00  am  Wakeup and morning routing, 7:00 am to 8:30 am  Excercice, 9:00 am to 9:30 am Breakfast and get ready for day 10:00 am to 1:00 pm learning Python, 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm Learning Machine Learning Algorithms, 4:00 pm to 4:30 pm short break, 4:30 pm to 6:00 pm learning DSA, 7:00 pm to 8:00 pm playing Guitar, 9:00 pm Dinner, 10:00 pm to 11:00 pm reading Book , 11:00 pm sleeping",
        "tuesday": "Boss, 6:00  am  Wakeup and morning routing, 7:00 am to 8:30 am  Excercice, 9:00 am to 9:30 am Breakfast and get ready for day 10:00 am to 1:00 pm learning Natural Language Processing, 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm Work on Personal Project, 4:00 pm to 4:30 pm short break, 4:30 pm to 6:00 pm solve Leetcode Questions, 7:00 pm to 8:00 pm playing Chess, 9:00 pm Dinner, 10:00 pm to 11:00 pm reading Book , 11:00 pm sleeping",
        "wednesday": "Boss, 6:00  am  Wakeup and morning routing, 7:00 am to 8:30 am Excercice, 9:00 am to 9:30 am Breakfast and get ready for day 10:00 am to 1:00 pm learning Computer Vision, 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm Work on Personal Project, 4:00 pm to 4:30 pm short break, 4:30 pm to 6:00 pm solve Hacker rank question, 7:00 pm to 8:00 pm playing Badminton, 9:00 pm Dinner, 10:00 pm to 11:00 pm reading Book , 11:00 pm sleeping",
        "thursday": "Boss, 6:00  am  Wakeup and morning routing, 7:00 am to 8:30 am  Excercice, 9:00 am to 9:30 am Breakfast and get ready for day 10:00 am to 1:00 pm learning Generative AI, 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm Work on Personal Project, 4:00 pm to 4:30 pm short break, 4:30 pm to 6:00 pm Learning DSA, 7:00 pm to 8:00 pm Watching Web series, 9:00 pm Dinner, 10:00 pm to 11:00 pm reading Book , 11:00 pm sleeping",
        "friday": "Boss, 6:00  am  Wakeup and morning routing, 7:00 am to 8:30 am  Excercice, 9:00 am to 9:30 am Breakfast and get ready for day 10:00 am to 1:00 pm  learning SQL And Vector Database, 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm Work on Personal Project, 4:00 pm to 4:30 pm short break, 4:30 pm to 6:00 pm Learning Machine Learning Alorithms, 7:00 pm to 8:00 pm playing Guitar, 9:00 pm Dinner, 10:00 pm to 11:00 pm reading Book , 11:00 pm sleeping",
        "satuarday": "Boss, 7:00  am  Wakeup and morning routing, 8:00 am to 9:30 am  Excercice, 9:30 am to 10:00 am Breakfast and get ready for day ,10:00 am to 1:00 pm Work on Personal Project , 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm  Work on Personal Project, 4:00 pm  to 4:30 pm short break, 4:30 pm to 6:00 pm Playing Video game, 7:00 pm to 8:00 pm Chilling With Friends, 9:00 pm Dinner, 10:00 pm to 12:00 pm Watching Web series , 12:00 pm sleeping",
        "sunday": "Boss, 7:00  am  Wakeup and morning routing, 8:00 am to 9:30 am Excercice, 9:30 am to 10:00 am Breakfast and get ready for day ,10:00 am to 12:00 pm Playing UNO With family , 1:00 pm to 2:00 pm Lunch, 2:00 pm to 4:00 pm Work on Personal Project, 4:00 pm to 4:30 pm short break, 4:30 pm to 6:00 pm Prepare for the upcoming week planning, 7:00 pm to 8:00 pm  Chilling With Friends, 9:00 pm Dinner, 10:00 pm to 11:00 pm Watching Web series , 11:00 pm sleeping",
    }
    if day in week.keys():
        speak(week[day])


def openApp(command):
    if "calculator" in command:
        subprocess.Popen(["calc.exe"])
        speak("Calculator opened")

    elif "notepad" in command:
        speak("Notepad opened")
        os.startfile("C:\\Windows\\System32\\notepad.exe")

    elif "paint" in command:
        subprocess.Popen(["mspaint.exe"])
        speak("Paint opened")


def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system("taskkill /f /im notepad.exe")
    elif "paint" in command:
        speak("closing paint")
        os.system("taskkill /f /im mspaint.exe")


def browsing(query):
    if "google" in query:
        speak("Boss, what should i search on google..")
        s = command()
        webbrowser.open(f"{s}")
    elif "spotify" in query:
        speak("Boss, what should i search on spotify..")
        s = command()
        webbrowser.open(f"https://open.spotify.com/search/{s}")

    elif "youtube" in query:
        speak("Boss, what should i search on youtube..")
        s = command()
        webbrowser.open(f"https://www.youtube.com/results?search_query={s}")
        speak("Here are some videos related to your search.")


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage >= 80:
        speak("Boss we could have enough charging to countinue your work")
    elif percentage >= 40 and percentage <= 75:
        speak(
            "Boss we should connect our system to charging point to charge your battery"
        )
    else:
        speak("Boss we have very low power, please connect to charging point")


# Spotify credentials
SPOTIFY_CLIENT_ID = "94d8687f0ca342679c94d295e418ce32"
SPOTIFY_CLIENT_SECRET = "4c142f31ecb2496daa2c2b3b0b61450a"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback/"

# Set up the Spotify OAuth
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state",
)

sp = spotipy.Spotify(auth_manager=sp_oauth)


def play_music_on_spotify(query):
    results = sp.search(q=query, type="track", limit=1)
    tracks = results["tracks"]["items"]

    if tracks:
        track = tracks[0]
        track_id = track["id"]
        track_name = track["name"]
        track_artist = track["artists"][0]["name"]
        speak(f"Playing {track_name} by {track_artist} on Spotify")

        # Get the current device ID
        devices = sp.devices()
        if devices["devices"]:
            device_id = devices["devices"][0]["id"]
            sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])
        else:
            speak("No active device found to play the music.")
    else:
        speak("Couldn't find the song on Spotify.")


def start_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Could not open the webcam.")
        return

    speak("Starting the webcam.")

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to capture image.")
            break

        cv2.imshow("Webcam", frame)

        # Press 'q' to exit the webcam window
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    speak("Webcam closed.")


def close_webcam():
    global webcam_active
    if webcam_active:
        webcam_active = False
        speak("Closing the webcam.")
    else:
        speak("Webcam is not currently active.")


def take_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Could not open the webcam.")
        return

    speak("Taking a photo.")

    ret, frame = cap.read()
    if ret:
        photo_filename = "photo.png"
        cv2.imwrite(photo_filename, frame)
        speak(f"Photo saved as {photo_filename}.")
    else:
        speak("Failed to capture photo.")

    cap.release()
    cv2.destroyAllWindows()


def get_weather(city):
    api_key = "2b2401e73a6e3ffb9c0f5e9dbbcf4982"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        temp = main.get("temp", "N/A")
        pressure = main.get("pressure", "N/A")
        humidity = main.get("humidity", "N/A")
        description = weather.get("description", "N/A")
        return {
            "temperature": temp,
            "pressure": pressure,
            "humidity": humidity,
            "description": description,
        }
    else:
        return None


# Function to report weather
def weather_report():
    speak("Boss, please tell me the city name.")
    city = command().lower()
    weather_info = get_weather(city)
    if weather_info:
        temperature = (
            weather_info["temperature"] - 273.15
        )  # Convert from Kelvin to Celsius
        speak(
            f"Current weather in {city} is {weather_info['description']}. "
            f"The temperature is {temperature:.2f} degrees Celsius. "
            f"The pressure is {weather_info['pressure']} hPa and "
            f"the humidity is {weather_info['humidity']}%."
        )
    else:
        speak(
            "Sorry, I couldn't fetch the weather information. Please try again later."
        )


if __name__ == "__main__":
    wishMe()

    while True:
        query = command().lower()
        # query = input("Enter your command: ")
        if (
            ("facebook" in query)
            or ("discord" in query)
            or ("whatsapp" in query)
            or ("instagram" in query)
            or ("twitter" in query)
            or ("linkedin" in query)
            or ("gmail" in query)
            or ("youtube" in query)
        ):
            social_media(query)

        elif ("daily time table" in query) or ("schedule" in query):
            schedule()

        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decreased")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")

        elif (
            ("open calculator" in query)
            or ("open notepad" in query)
            or ("open paint" in query)
        ):
            openApp(query)

        elif (
            ("close calculator" in query)
            or ("close notepad" in query)
            or ("close paint" in query)
        ):
            closeApp(query)

        elif (
            ("what" in query)
            or ("who" in query)
            or ("hu" in query)
            or ("when" in query)
            or ("it was" in query)
            or ("haha" in query)
            or ("make me" in query)
            or ("how" in query)
            or ("hi" in query)
            or ("thanks" in query)
            or ("hello" in query)
            or ("joke" in query)
            or ("bye" in query)
            or ("Great" in query)
            or ("good talk" in query)
        ):
            padded_sequences = pad_sequences(
                tokenizer.texts_to_sequences([query]), maxlen=20, truncating="post"
            )
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data["intents"]:
                if i["tag"] == tag:
                    speak(np.random.choice(i["responses"]))

        elif (
            ("open google" in query)
            or ("open spotify" in query)
            or ("open youtube" in query)
        ):
            browsing(query)

        elif ("system conditions" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()

        elif "play song" in query and "spotify" in query:
            speak("Boss, what should I play on Spotify?")
            s = command()
            play_music_on_spotify(s)

        elif "start webcam" in query or "open webcam" in query:
            start_webcam()

        elif "take photo" in query or "capture photo" in query:
            take_photo()

        elif "close webcam" in query:
            close_webcam()

        if "weather" in query:
            weather_report()

        elif "exit" in query:
            sys.exit()


# speak("hello, I'm NOVA")
