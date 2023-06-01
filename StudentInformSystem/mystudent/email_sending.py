from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def send_email(request):
    subject = 'Test email'
    message = 'Hello!'
    from_email = 'artefact453@gmail.com'
    recipient_list = ['artefact032@yandex.ru',]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return