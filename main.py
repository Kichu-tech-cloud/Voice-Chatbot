import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv
from difflib import get_close_matches

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Predefined questions and answers
predefined_qna = {
    "what should we know about your life story in a few sentences?":
        "I am a passionate and adaptable individual with a strong interest in AI and machine learning, eager to learn and contribute to meaningful projects.",
    "what's your superpower?":
        "I excel at learning quickly, embracing change, and never giving up easily.",
    "what are the top 3 areas you'd like to grow in?":
        "Deepening my expertise in artificial intelligence, machine learning, and data science.",
    "what misconception do your coworkers have about you?":
        "Some think I'm too serious, but I value humor and enjoy team collaboration.",
    "how do you push your boundaries and limits?":
        "I analyze feedback, embrace challenges, learn from mistakes, and set ambitious goals to push myself further."
}

# Normalize text for comparison
def normalize_text(text):
    return text.strip().lower()

# Recognize speech from microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak into the microphone.")
        try:
            audio = recognizer.listen(source, timeout=10)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Error with speech recognition service."

# Convert text to speech and play
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        temp_audio = "response.mp3"
        tts.save(temp_audio)
        st.audio(temp_audio, format="audio/mp3")
        os.remove(temp_audio)  # Cleanup temporary file
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")

# Query OpenAI API
def query_openai(user_query):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_query,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error with OpenAI API: {e}"

# Find the closest predefined answer
def get_closest_predefined_answer(user_query):
    normalized_query = normalize_text(user_query)
    normalized_keys = {normalize_text(key): value for key, value in predefined_qna.items()}
    matches = get_close_matches(normalized_query, normalized_keys.keys(), n=1, cutoff=0.5)
    if matches:
        return normalized_keys[matches[0]]
    return "I don't have an answer for that question."

# Streamlit UI
def main():
    st.title("Voicemuse")
    st.write("Speak into the microphone to interact with the bot.")

    if st.button("Start Listening"):
        user_query = recognize_speech()
        if user_query:
            st.write(f"You said: {user_query}")
            if openai.api_key:
                response = query_openai(user_query)
                if "Error with OpenAI API" in response:
                    response = get_closest_predefined_answer(user_query)
            else:
                response = get_closest_predefined_answer(user_query)

            st.write(f"Chatbot: {response}")
            speak(response)

if __name__ == "__main__":
    main()
