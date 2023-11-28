from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
client = OpenAI()

def mcqs_from_audio(audio_path):
    audio_file= open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcript.text

