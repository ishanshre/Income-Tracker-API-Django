from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from accounts.models import User
from accounts.token import account_activation_token
from accounts.email import send_activation_email

def activate(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    current_site = get_current_site(request).domain
    email_verification_relative_path = reverse("accounts:email_verify")
    activation_url = "http://"+current_site+email_verification_relative_path+"?uidb64="+str(uid)+"&token="+str(token)
    send_activation_email(activation_url=activation_url, to_email=user.email, username=user.username)


def verify(request):
    uidb64 = request.GET.get('uidb64')
    token = request.GET.get('token')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user=user, token=token):
        user.is_email_confirmed = True
        user.save()
        return True
    else:
        return False
