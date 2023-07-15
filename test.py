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
        print("Recording started. Speak now...")
        audio = r.listen(source)
        print("Recording finished.")
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
    speak_message("Please speak your location in terms of latitude and longitude. Thank you.")
    play_startup_tone()
    while True:
        audio = record_audio()
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio)
            print("Spoken text:", text)
            latitude, longitude = extract_lat_long_from_text(text)
            print("The latitude and longitude of the speaker is: {}, {}".format(latitude, longitude))
        except sr.UnknownValueError:
            print("Unable to recognize speech.")
        except sr.RequestError as e:
            print("Speech recognition service error:", e)
        
        choice = input("Press '1' to exit or any other key to continue: ")
        if choice == "1":
            break

if __name__ == "__main__":
    main()
