import io
import wave
import sounddevice as sd
import RPi.GPIO as GPIO
import requests
import json
import serial
import time

# Button pin
button_pin = 5

# Speech API key, location, and language
speech_api_key = 'de1c6cd6162e4fed86a8c459b926a2fd'
sentiment_api_key = '80880f027a514db2a1d7eb8c6e43f2ae'
sentiment_api_endpoint = 'https://rachelsface.cognitiveservices.azure.com/'
location = 'uksouth'
language = 'en-GB'

# Serial communication setup for Arduino
arduino_port = '/dev/ttyACM0'
arduino_baudrate = 9600
arduino_timeout = 1

ser = serial.Serial(arduino_port, arduino_baudrate, timeout=arduino_timeout)

# Function to get access token for speech API
def get_speech_access_token():
    headers = {
        'Ocp-Apim-Subscription-Key': speech_api_key
    }
    token_endpoint = f'https://{location}.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
    response = requests.post(token_endpoint, headers=headers)
    return str(response.text)

# Function to get access token for sentiment API
def get_sentiment_access_token():
    headers = {
        'Ocp-Apim-Subscription-Key': sentiment_api_key
    }
    token_endpoint = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
    response = requests.post(token_endpoint, headers=headers)
    return str(response.text)

# Function to convert speech to text using the Speech API
def convert_speech_to_text(buffer):
    url = f'https://{location}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1'
    headers = {
        'Authorization': 'Bearer ' + get_speech_access_token(),
        'Content-Type': f'audio/wav; codecs=audio/pcm; samplerate={rate}',
        'Accept': 'application/json;text/xml'
    }
    params = {
        'language': language
    }
    response = requests.post(url, headers=headers, params=params, data=buffer)
    response_json = response.json()
    if response_json['RecognitionStatus'] == 'Success':
        return response_json['DisplayText']
    else:
        return ''

# Function to perform sentiment analysis using the Sentiment Analysis API
def perform_sentiment_analysis(text):
    headers = {
        'Authorization': 'Bearer ' + get_sentiment_access_token(),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'documents': [
            {
                'id': '1',
                'language': language,
                'text': text
            }
        ]
    }
    response = requests.post(sentiment_api_endpoint, headers=headers, json=data)
    response_json = response.json()
    if 'documents' in response_json:
        sentiment_score = response_json['documents'][0]['sentiment']
        return sentiment_score
    else:
        return 'unknown'

# Function to process the sentiment result
def process_sentiment(sentiment):
    emotions_mapping = {
        'positive': 7,  # unknown
        'neutral': 6,   # unknown
        'negative': {
            'anger': 1,
            'sadness': 2,
            'shock': 3,
            'fear': 4,
            'confusion': 5
        }
    }
    if sentiment in emotions_mapping['negative']:
        emotion_code = emotions_mapping['negative'][sentiment]
        print(f"Detected emotion: {emotion_code}")
        # Send the emotion code to Arduino
        send_to_arduino(emotion_code)
    else:
        print("Detected emotion: unknown")

# Function to send data to Arduino
def send_to_arduino(emotion_code):
    try:
        ser.write(str(emotion_code).encode())
        print(f"Emotion code {emotion_code} sent to Arduino.")
    except Exception as e:
        print(f"Error sending data to Arduino: {e}")

# Function to capture audio using sounddevice
def capture_audio():
    frames = []
    with sd.InputStream(channels=1, dtype='int16', samplerate=rate) as stream:
        print("Recording... Press the button to stop.")
        while GPIO.input(button_pin) == GPIO.LOW:
            data, overflowed = stream.read(4096)
            frames.append(data)
        print("Recording stopped.")
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wavefile:
        wavefile.setnchannels(1)
        wavefile.setsampwidth(2)  # 2 bytes for int16
        wavefile.setframerate(rate)
        wavefile.writeframes(b''.join(frames))
        wav_buffer.seek(0)
    return wav_buffer

# Audio parameters
rate = 48000

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    # Wait for the button press
    GPIO.wait_for_edge(button_pin, GPIO.FALLING)

    # Capture audio
    buffer = capture_audio()

    # Convert speech to text
    text = convert_speech_to_text(buffer)

    # Perform sentiment analysis
    sentiment = perform_sentiment_analysis(text)

    # Process the sentiment
    process_sentiment(sentiment)

    # Delay to avoid rapid button presses
    time.sleep(1)
