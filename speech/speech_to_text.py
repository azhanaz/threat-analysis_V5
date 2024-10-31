import speech_recognition as sr

# Initialize recognizer class
recognizer = sr.Recognizer()

def convert_speech_to_text():
    # Use the default microphone as input
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error with speech recognition service; {0}".format(e)
