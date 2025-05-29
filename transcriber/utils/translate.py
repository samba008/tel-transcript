from deep_translator import GoogleTranslator

def translate_text_to_telugu(text):
    if len(text) > 5000:
        return "[Translation skipped: text too long]"
    return GoogleTranslator(source='auto', target='te').translate(text)
