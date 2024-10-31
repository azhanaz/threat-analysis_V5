import speech_recognition as sr
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# Load the fine-tuned model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained('./threat_model')
tokenizer = DistilBertTokenizer.from_pretrained('./threat_model')

def analyze_threat(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return "threat" if predicted_class == 1 else "non-threat"

def recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something... (You have 5 seconds to speak)")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Set a 5-second timeout
            print("Recording complete.")
            # Use Google Web Speech API to recognize the speech
            speech_text = recognizer.recognize_google(audio)
            print(f"You said: {speech_text}")
            return speech_text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

if __name__ == "__main__":
    # Recognize speech
    spoken_text = recognize_speech()
    
    if spoken_text:
        # Analyze the threat
        result = analyze_threat(spoken_text)
        # Print the result
        print(f"The analysis result for the input is: {result}")
