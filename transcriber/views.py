from django.shortcuts import render
from .forms import MediaUploadForm
import cloudinary.uploader
from .utils.assembly import transcribe_with_diarization
from .utils.translate import translate_text_to_telugu

def upload_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Upload media to Cloudinary
            file = form.cleaned_data['media_file']
            upload_result = cloudinary.uploader.upload_large(file, resource_type="video")
            url = upload_result.get("secure_url")

            # Transcribe the media
            result = transcribe_with_diarization(url)
            utterances = result.get("utterances", [])

            # Translate each utterance to Telugu
            for u in utterances:
                u['telugu'] = translate_text_to_telugu(u['text'])

            return render(request, 'result.html', {
                'utterances': utterances,
                'url': url
            })
    else:
        form = MediaUploadForm()

    return render(request, 'upload.html', {'form': form})
