import speech_recognition as sr
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# Load the fine-tuned model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained('./threat_model')
tokenizer = DistilBertTokenizer.from_pretrained('./threat_model')

def analyze_threat(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    # Get model outputs
    outputs = model(**inputs)
    logits = outputs.logits
    
    # Get the predicted class (0 for non-threat, 1 for threat)
    predicted_class = torch.argmax(logits, dim=1).item()
    return "threat" if predicted_class == 1 else "non-threat"

def recognize_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please speak something...")
        # Adjust for ambient noise and record
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Use Google Web Speech API to recognize the audio
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

if __name__ == "__main__":
    spoken_text = recognize_speech()  # Capture speech input
    if spoken_text:
        result = analyze_threat(spoken_text)  # Analyze the threat
        print(f"The analysis result for the input is: {result}")  # Print the result
