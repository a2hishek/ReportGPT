import speech_recognition as sr
import base64

def record_audio():
    recogniser = sr.Recognizer()

    with sr.Microphone() as source:
        recogniser.adjust_for_ambient_noise(source, duration=1)
        audio_data = recogniser.listen(source, timeout=10)
        audio = audio_data.get_wav_data()
        audio_data = base64.b64encode(audio).decode("utf-8")

        return audio_data
