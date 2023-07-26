#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
# import openai

# openai.api_key="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"

# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content": "write an wssay about penguins"}])
# print(completion.choices[0].message.content)
import openai
import pyttsx3
import speech_recognition as sr
import webbrowser

# Set up OpenAI API key
openai.api_key = "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"

# Create OpenAI completion object
completion = openai.Completion()

def reply(question):
    prompt = f'Jarvis: {question}\n User: '
    response = completion.create(prompt=prompt, engine="text-davinci-002", stop=['User'], max_tokens=200)
    answer = response.choices[0].text.strip()
    return answer

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Hello, I am Jarvis. How can I assist you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing.....")
        query = recognizer.recognize_google(audio, language='en-in')
        print("User Said: {} \n".format(query))
    except Exception as e:
        print("Say That Again....")
        return "None"
    return query


if __name__ == '__main__':
    while True:
        query = take_command().lower()
        if 'exit' in query:
            speak("Goodbye. Have a great day!")
            break
        response = reply(query)
        print("Jarvis: {}".format(response))
        speak(response)
        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("www.google.com")
