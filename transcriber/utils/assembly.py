# transcriber/utils/assembly.py

import requests
import time

API_KEY = "7e61a69b93854cff83a51717dd68534e"

upload_url = "https://api.assemblyai.com/v2/transcript"
headers = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

def transcribe_with_diarization(audio_url):
    response = requests.post(upload_url, json={
        "audio_url": audio_url,
        "speaker_labels": True,
        "language_code": "en"
    }, headers=headers)

    transcript_id = response.json()["id"]
    polling_url = f"{upload_url}/{transcript_id}"

    while True:
        poll_response = requests.get(polling_url, headers=headers)
        status = poll_response.json()["status"]
        if status == "completed":
            return poll_response.json()
        elif status == "error":
            raise Exception(f"Transcription failed: {poll_response.json()['error']}")
        time.sleep(3)
