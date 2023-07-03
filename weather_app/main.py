import requests
import json
import pyttsx3


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    while True:

        city = input("Enter name of city \n")
        if city == 'q':
                    break
        
        url = f"http://api.weatherapi.com/v1/current.json?key=4b16fc7384024066a6584319230307&q={city}"

        r = requests.get(url)

        wdic = json.loads(r.text)
        w = wdic["current"] ["temp_c"]
        
        print(f"the current weather in {city} is {w} degrees.")
        speak_text(f"say 'the current weather in {city} is {w} degrees'")

       