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

    response.raise_for_status()  # <- catch bad request errors early

    transcript_id = response.json().get("id")
    if not transcript_id:
        raise Exception("No transcript ID received from AssemblyAI")

    polling_url = f"{upload_url}/{transcript_id}"

    while True:
        poll_response = requests.get(polling_url, headers=headers)
        poll_response.raise_for_status()

        result_json = poll_response.json()
        status = result_json.get("status")

        if status == "completed":
            if "utterances" not in result_json:
                raise Exception("No utterances found in completed transcript")
            return result_json

        elif status == "error":
            raise Exception(f"Transcription failed: {result_json.get('error')}")

        time.sleep(3)
