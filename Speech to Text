import io
import wave
import sounddevice as sd
import RPi.GPIO as GPIO
import requests

# Button pin 
button_pin = 5

# Speech API key, location, and language
speech_api_key = 'de1c6cd6162e4fed86a8c459b926a2fd'
location = 'uksouth'
language = 'en-GB'

# Function to get access token for speech API
def get_access_token():
    headers = {
        'Ocp-Apim-Subscription-Key': speech_api_key
    }
    token_endpoint = f'https://{location}.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
    response = requests.post(token_endpoint, headers=headers)
    return str(response.text)

# Function to convert speech to text using the REST API
def convert_speech_to_text(buffer):
    url = f'https://{location}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1'
    headers = {
        'Authorization': 'Bearer ' + get_access_token(),
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

# Function to process the text
def process_text(text):
    print(text)

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
    
    # Process the text
    process_text(text)
