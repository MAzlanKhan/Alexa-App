from openai import OpenAI
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
import webbrowser
import pyttsx3
import subprocess
import os
import pygame
import youtubeData
import softwares


# --Sign Up--

# File to store user data
DATABASE_FILE = "database.txt"

# Function to save user data
def save_user_data(name, email):
    with open(DATABASE_FILE, "a") as file:
        file.write(f"{name}, {email}\n")  # Append new user details

# Initialize session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# User Input Form
if not st.session_state.user_name or not st.session_state.user_email:
    st.title("Enter Your Details")
    name = st.text_input("Name", key="name")
    email = st.text_input("Email", key="email")

    if st.button("Submit"):
        if name and email:
            st.session_state.user_name = name
            st.session_state.user_email = email
            
            # Save data to database file
            save_user_data(name, email)
            
            # st.experimental_rerun()  # Refresh the app
        else:
            st.warning("Please enter both name and email.")
else:
    st.title(f"Welcome, {st.session_state.user_name}!")
    st.write(f"Your Email: {st.session_state.user_email}")



    # ---- Main app content-----

    r = sr.Recognizer()
    engine = pyttsx3.init()
    st.title("Alexa Here!") # Title
 
    # SPEAK FUNCTION 
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # NEW SPEAK FUNCTION USING GTTS
    def speak_new(text):
        tts = gTTS(text)
        tts.save('newvoice.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load("newvoice.mp3")  # Replace with your MP3 file path
        st.success(text)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Check if music is still playing
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()  # Replace with your MP3 file path
        os.remove("newvoice.mp3")

    # OPEN AI FUNCTION 
    Code Removed 

    # HANDLE MANUALL COMMANDS  
    def process_command(command):
        # Social Accounts
        if "google" in command.lower():
            webbrowser.open("https://www.google.com/")
        elif "facebook" in command.lower():
            webbrowser.open("https://www.facebook.com/")
        elif "instagram" in command.lower():
            webbrowser.open("https://www.instagram.com/")
        elif "linkedin" in command.lower():
            webbrowser.open("https://www.linkedin.com/in/azlan-khan-00173b340/")
        elif "youtube" in command.lower():
            webbrowser.open("https://www.youtube.com/")
        elif "github" in command.lower():
            webbrowser.open("https://github.com/MAzlanKhan")
        elif "gpt" in command.lower():
            webbrowser.open("https://chatgpt.com/")
        
        # Courses
        elif command.lower().startswith("course"):
            course = command.lower().split(" ")[1]
            course_link = youtubeData.courses[course]
            webbrowser.open(course_link)

        # Softwares 
        elif command.lower().startswith("app"):
            software = command.lower().split(" ")[1]
            software_link = softwares.software[software]
            subprocess.run([software_link])

        # OPEN AI
        else:
            output = openai(command)
            speak_new(output)



    if __name__ == "__main__": 
        speak_new("Initializing Alexa...") # First Impression
        while True:

                try:
                    with sr.Microphone() as source:
                        st.warning("Listening...")
                        audio = r.listen(source, timeout=2, phrase_time_limit=1)     
                    word = r.recognize_google(audio) # recognize speech using Google Cloud
                    
                    if "alexa" in word.lower():
                        speak_new("Ya")
                        with sr.Microphone() as source:
                            st.success("Alexa Activated...")

                            # check syntax for confirmation 
                            audio = r.listen(source, timeout=2, phrase_time_limit=4)
                            command = r.recognize_google(audio) # recognize speech using Google Cloud
                            process_command(command)
                            
                except Exception as e:
                    print("Error; {0}".format(e))