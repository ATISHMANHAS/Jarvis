import speech_recognition as sr
import pyttsx3
import requests
import time

# Initialize text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Listen for commands from the microphone
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

# Function to ask a question using OpenAI API
def ask_question(question):
    api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Specify the model you want to use
        'messages': [{'role': 'user', 'content': question}]
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        return answer
    else:
        return "Sorry, I couldn't get an answer to that."

# Reminder storage
reminders = []

# Function to set a reminder
def set_reminder(reminder):
    reminders.append(reminder)
    speak(f"Reminder set for: {reminder}")

# Function to check reminders
def check_reminders():
    if reminders:
        speak("Here are your reminders:")
        for reminder in reminders:
            speak(reminder)
    else:
        speak("You have no reminders.")

# Main loop to listen for commands
while True:
    command = listen_for_commands()
    if command:
        if "hello" in command.lower():
            speak("Hello! How can I assist you?")
        elif "time" in command.lower():
            current_time = time.strftime("%H:%M")
            speak(f"The current time is {current_time}.")
        elif "remind me to" in command.lower():
            reminder = command.lower().replace("remind me to", "").strip()
            set_reminder(reminder)
        elif "show reminders" in command.lower():
            check_reminders()
        elif "what is" in command.lower():
            question = command.lower().replace("what is", "").strip()
            answer = ask_question(question)
            speak(answer)
        elif "stop" in command.lower():
            speak("Goodbye!")
            break
