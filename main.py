import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from dotenv import load_dotenv
from difflib import get_close_matches




load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


predefined_qna = {
    "what should we know about your life story in a few sentences?":
        "I am a passionate and adaptable individual with strong interest in AI and machine learning, eager to learn and contribute to meaningful projects. ",
    "what's your super power?":
        "I excel at learning quickly, embracing change, and never giving up easily.",
    "what are the top 3 areas you'd like to grow in?":
        "Deepening my expertise in artificial intelligence, machine learning, and data science.",
    "what misconception do your coworkers have about you?":
        "Some think I'm too serious, but I value humor and enjoy team collaboration.",
    "how do you push your boundaries and limits?":
        "I analyze feedback, embrace challenges, learn from mistakes, and set ambitious goals to push myself further."
}


def normalize_text(text):
    return text.strip().lower()


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


def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    st.audio("response.mp3", format="audio/mp3")


def query_openai(user_query):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_query,
            max_tokens=100
        )
        return response.choices[0].strip()
    except Exception as e:
        return f"Error with OpenAI API: {e}"


def get_closet_predefined_answer(user_query):
    normalized_query = normalize_text(user_query)
    normalized_keys = {normalize_text(key): value for key, value in predefined_qna.items()}
    matches = get_close_matches(normalized_query, normalized_keys.keys(), n=1, cutoff=0.5)
    if matches:
        return normalized_keys[matches[0]]
    return "I don't have an answer for that question."


def main():
    st.title("Voicemuse")
    st.write("Speak into the microphone to interact with the bot.")

    if st.button("Start Listening"):
        user_query = recognize_speech()
        if user_query:
            st.write(f"You said: {user_query}")


            if openai.api_key:
                response = query_openai(user_query)
                if "Error with OpenAI API: in response:":

                    response = get_closet_predefined_answer(user_query)
            else:

                response = get_closet_predefined_answer(user_query)

            st.write(f"Chatbot: {response}")
            speak(response)

if __name__ == "__main__":
    main()
