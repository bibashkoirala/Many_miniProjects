import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    while True:
        input_text = input("Enter the text you want to speak: ")
        if input_text == 'q':
            break
        speak_text(input_text)