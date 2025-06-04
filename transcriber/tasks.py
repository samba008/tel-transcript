from celery import shared_task
from .utils.assembly import transcribe_with_diarization
from .utils.translate import translate_text_to_telugu

from django.conf import settings
import tempfile
import os
# tasks.py
import logging

logger = logging.getLogger(__name__)
from django.core.mail import EmailMessage


@shared_task(bind=True)
def process_and_email_transcription(self, file_url, user_email):
    try:
        logger.info(f"[TASK START] Transcribing file from URL: {file_url}")

        result = transcribe_with_diarization(file_url)
        utterances = result.get("utterances")
        if not utterances:
            raise ValueError("No utterances returned from API")

        for u in utterances:
            u["telugu"] = translate_text_to_telugu(u["text"])

        transcript_text = "\n\n".join(
            [f"Speaker {u['speaker']}:\nEnglish: {u['text']}\nTelugu: {u['telugu']}" for u in utterances]
        )

        file_path = f"transcript_{user_email}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        email = EmailMessage(
            subject="Your Transcription is Ready",
            body="Please find the transcription attached.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        email.attach_file(file_path)
        email.send()

        os.remove(file_path)
        logger.info(f"[TASK DONE] Transcription emailed to {user_email}")
        return "Transcription complete and email sent"

    except Exception as e:
        logger.error(f"[TASK ERROR] {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60, max_retries=3)
