from django.core.mail import send_mail


def send_confirmation_code(email, code):
    params = {
        'subject': 'Код подтверждния',
        'message': code,
        'from_email': '',
        'recipient_list': [email],
    }
    send_mail(**params)
