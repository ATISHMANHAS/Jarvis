import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr

# Set up the API key and search engine ID directly in the code
API_KEY = "AIzaSyCRpTG2IOVryOIyCfJHIMsx1wbbNRS5ZFg"  # Your Google API Key
SEARCH_ENGINE_ID = "d523ad25757f44b96"  # Your Google Search Engine ID
genai.configure(api_key=API_KEY)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def set_voice_by_name(name):
    """Set the TTS voice to one matching the given name."""
    voices = engine.getProperty('voices')
    for voice in voices:
        if name.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            print(f"Using voice: {voice.name}")
            return
    print("Voice not found, using default.")

def list_available_voices():
    """List available TTS voices."""
    voices = engine.getProperty('voices')
    print("Available voices:")
    for voice in voices:
        print(f"- {voice.name}")

def speak(text, rate=150):
    """Convert text to speech."""
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for a command and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from the service.")
        return None

def change_voice(command):
    """Change the voice based on user command."""
    if "change voice to" in command.lower():
        voice_name = command.lower().replace("change voice to ", "")
        set_voice_by_name(voice_name)

def generate_response(command):
    """Generate a response using the Generative AI API."""
    model = genai.GenerativeModel("gemini-1.5-flash")  # Adjust the model name if needed
    response = model.generate_content(command)
    return response.text

def main():
    set_voice_by_name("Microsoft Zira Desktop")  # Default voice

    while True:
        print("Please say your command (type 'exit' to quit):")
        command = take_command()
        if command is None:
            continue  # Retry if command was not understood
        if command.lower() == "exit":
            speak("Goodbye!")
            break

        # Change voice if the command is recognized
        change_voice(command)

        # List available voices
        if command.lower() == "list voices":
            list_available_voices()
            continue

        # Generate content using the Generative AI
        response_text = generate_response(command)

        # Print and speak the generated content
        print("Generated Content:")
        print(response_text)
        speak(response_text, rate=180)  # Adjust the speech rate here as needed

if __name__ == "__main__":
    main()
