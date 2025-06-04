from django.core.mail import EmailMessage
from django.conf import settings

email = EmailMessage(
    subject='Test',
    body='It works!',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=['yourgmail@example.com']
)
email.send()
