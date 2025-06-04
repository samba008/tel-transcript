from django import forms

class MediaUploadForm(forms.Form):
    media_file = forms.FileField(label="Upload Audio or Video File")
    email = forms.EmailField(label="Your Email Address")
