from django.core.mail import EmailMessage


def send_email(actual_url, to_email, username, action):
    if action == "register":
        subject = "Activate your Income and Expences Tracker account"
        message = f'''
        Hello {username.title()}! Please open the following link to confirm email in your account
        {actual_url}
        '''

    elif action == "resend_email_verify":
        subject = "Verify your Income and Expences Tracker account email"
        message = f'''
        Hello {username.title()}! Please open the following link to confirm email in your account
        {actual_url}
        '''
    elif action == "reset_password":
        subject = "Reset Your account"
        message = f'''
        Hello {username.title()}! Please open the link to rest your password\n
        {actual_url}\n
        If your did not apply for password rest then please ignore it and this is to inform you that some has applied to reset your account using email
        '''
    email = EmailMessage(
            subject, message, to=[to_email]
    )
    email.send()