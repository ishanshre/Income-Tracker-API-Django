from django.core.mail import EmailMessage


def send_activation_email(activation_url, to_email, username):
    subject = "Activate your Income and Expences Tracker account"
    message = f'''
    Hello {username.title()}! Please open the following link to activate your account
    {activation_url}
    '''
    email = EmailMessage(
        subject, message, to=[to_email]
    )
    email.send()
    
    