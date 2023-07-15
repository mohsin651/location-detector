import streamlit as st
import speech_recognition as sr
import pygame
import pyttsx3

def play_startup_tone():
    pygame.mixer.init()
    pygame.mixer.music.load('sound.mp3')
    pygame.mixer.music.play()

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Recording started. Speak now...")
        audio = r.listen(source)
        st.write("Recording finished.")
    return audio

def extract_lat_long_from_text(text):
    words = text.split()
    latitude = ""
    longitude = ""
    
    for word in words:
        if word.replace('.', '', 1).isdigit():  # Check if the word is a number
            if latitude == "":
                latitude = word
            else:
                longitude = word
                break  # Exit the loop after finding the second number
    
    return latitude, longitude

def speak_message(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speech rate
    engine.setProperty('volume', 0.8)  # You can adjust the volume
    engine.say(message)
    engine.runAndWait()

def main():
    st.title("Latitude and Longitude Detection")
    st.write("Press the Start button to begin recording.")

    if st.button("Start"):
        speak_message("Please speak your location in terms of latitude and longitude. Thank you.")
        play_startup_tone()
        audio = record_audio()
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio)
            st.write("Spoken text:", text)
            latitude, longitude = extract_lat_long_from_text(text)
            st.write("The latitude and longitude of the speaker is: {}, {}".format(latitude, longitude))
        except sr.UnknownValueError:
            st.write("Unable to recognize speech.")
        except sr.RequestError as e:
            st.write("Speech recognition service error:", e)

if __name__ == "__main__":
    main()
