from django.core.mail import send_mail

def send_reset_email(email, code):
    subject = 'Құпиясөзді қалпына келтіру коды'
    message = f'Сіздің растау кодыңыз: {code}'
    from_email = 'noreply@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
