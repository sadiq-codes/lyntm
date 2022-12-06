from django.shortcuts import render
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
# from dj_rest_auth.registration.views import  Re

from django_rest_passwordreset.signals import reset_password_token_created

from .models import CustomUser
from .serializers import CustomUserSerializer

account_sid = "AC517ca8eef720380cf2d604dce3650ab9"
auth_token = "dc82de7628d8cd33847e64ca5cac1dfd"
client = Client(account_sid, auth_token)


# Create your views here.

class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


@receiver(reset_password_token_created)
def email_password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key
    }
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="LYNTM"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@lyntm.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


@receiver(reset_password_token_created)
def sms_password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    token = reset_password_token.key
    phone_number = reset_password_token.user.phone_number

    try:
        message = client.messages.create(
            to=phone_number,
            from_="+18644289576",
            body=f'Hi, here is your reset password code {token}.\
                                     Don\'nt share this code with anyone; our employees will \
                never ask for it.'
        )
    except TwilioRestException as err:
        # Implement your fallback code here
        print(err)
