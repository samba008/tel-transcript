from django.shortcuts import render
from .forms import MediaUploadForm
import cloudinary.uploader
from .tasks import process_and_email_transcription

def upload_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['media_file']
            email = form.cleaned_data['email']

            # Upload file to Cloudinary
            upload_result = cloudinary.uploader.upload_large(file, resource_type="video")
            url = upload_result.get("secure_url")

            # Ensure it's a raw direct-access file
            if url:
                url = url.replace("/upload/", "/upload/fl_attachment/")

            # Trigger async task
            process_and_email_transcription.delay(url, email)

            return render(request, 'upload_success.html', {'email': email})
    else:
        form = MediaUploadForm()
    return render(request, 'upload.html', {'form': form})
