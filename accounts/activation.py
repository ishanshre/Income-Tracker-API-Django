from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from accounts.models import User
from accounts.token import account_activation_token
from accounts.email import send_email

def create_email(request, user, action):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    current_site = get_current_site(request).domain
    if action == "register":
        relative_path = reverse("accounts:email_verify")
    elif action == "resend_email_verify":
        relative_path = reverse("accounts:resend_email_verify")
    elif action == "reset_password":
        relative_path = reverse("accounts:reset_password")
    actual_url = "http://"+current_site+relative_path+"?uidb64="+str(uid)+"&token="+str(token)
    send_email(actual_url=actual_url, to_email=user.email, username=user.username, action=action)


def verify(request, action, **kwargs):
    uidb64 = request.GET.get('uidb64')
    token = request.GET.get('token')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user=user, token=token) and action == "email_verify":
        user.is_email_confirmed = True
        user.save()
        return True
    return False

def verify_token(uidb64, token, action):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user=user, token=token) and action == "reset_password":
        return True, uid
    elif user is not None and account_activation_token.check_token(user=user, token=token) and action == "resend_email_verify":
        return True, uid
    return False, None



