import os
import streamlit as st  # Importing the Streamlit library for creating the web application
import speech_recognition as sr  # Importing the SpeechRecognition library for speech recognition capabilities
import pygame  # Importing the Pygame library for playing startup tone
# import pyttsx3  # Importing the pyttsx3 library for text-to-speech conversion

def play_startup_tone():  # Function to play the startup tone sound
    pygame.mixer.init()  # Initialize the Pygame mixer
    pygame.mixer.music.load('sound.mp3')  # Load the startup tone sound file
    pygame.mixer.music.play()  # Play the startup tone sound

def record_audio():  # Function to recor audio from the microphone
    r = sr.Recognizer()  # Create a Recognizer object for speech recognition
    with sr.Microphone() as source:  # Use the microphone as the audio source
        st.write("Recording started. Speak now...")  # Display message indicating recording has started
        audio = r.listen(source)  # Listen for audio input from the microphone
        st.write("Recording finished.")  # Display message indicating recording has finished
    return audio  # Return the recorded audio

def extract_lat_long_from_text(text):  # Function to extract latitude and longitude from text
    words = text.split()  # Split the text into individual words
    latitude = ""  # Variable to store the latitude
    longitude = ""  # Variable to store the longitude

    for word in words:  # Iterate through each word in the text
        if word.replace('.', '', 1).isdigit():  # Check if the word is a number (latitude or longitude)
            if latitude == "":  # If latitude is empty, assign the current word as latitude
                latitude = word
            else:  # If latitude is already assigned, assign the current word as longitude
                longitude = word
                break  # Exit the loop after finding the second number (longitude)
    
    return latitude, longitude  # Return the extracted latitude and longitude

# def speak_message(message):  # Function to speak a given message using text-to-speech
#     engine = pyttsx3.init()  # Initialize the pyttsx3 engine for text-to-speech
#     engine.setProperty('rate', 150)  # Set the speech rate to 150 (you can adjust this value)
#     engine.setProperty('volume', 0.8)  # Set the speech volume to 0.8 (you can adjust this value)
#     engine.say(message)  # Queue the message for speech output
#     engine.runAndWait()  # Wait for the speech output to complete

def main():  # Main function to run the Streamlit application
    st.title("Latitude and Longitude Detection")  # Set the title of the application
    st.subheader("Record your location in terms of latitude and longitude.")  # Display a subheader

    start_button = st.button("Start")  # Create a button labeled "Start"
    latitude_output = st.empty()  # Create an empty output placeholder for latitude
    longitude_output = st.empty()  # Create an empty output placeholder for longitude

    if start_button:  # If the "Start" button is clicked
        # speak_message("Please speak your location in terms of latitude and longitude. Thank you.")  # Speak a message
        play_startup_tone()  # Play the startup tone
        audio = record_audio()  # Record audio from the microphone
        recognizer = sr.Recognizer()  # Create a Recognizer object for speech recognition
        try:
            text = recognizer.recognize_google(audio)  # Convert the recorded audio to text using Google Speech Recognition
            latitude, longitude = extract_lat_long_from_text(text)  # Extract latitude and longitude from the text

            with latitude_output:
                st.write("Spoken text:", text)  # Display the spoken text
                st.text_input("Latitude:", value=latitude)  # Display an input field for latitude

            with longitude_output:
                st.text_input("Longitude:", value=longitude)  # Display an input field for longitude
        except sr.UnknownValueError:  # If the speech cannot be recognized
            st.error("Unable to recognize speech.")  # Display an error message
        except sr.RequestError as e:  # If there is an error with the speech recognition service
            st.error("Speech recognition service error:", e)  # Display an error message

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
