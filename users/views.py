from django.shortcuts import render
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer, TwitterConnectSerializer

from django_rest_passwordreset.signals import reset_password_token_created

from .models import CustomUser
from .serializers import CustomUserSerializer, ImageSerializer

account_sid = "qwdnwobfo1h3uo13fjq"
auth_token = "r3ji10h3r013803r1qj"
client = Client(account_sid, auth_token)


# Create your views here.

class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProfileImage(APIView):

    def get(self, request, **kwargs):
        user = CustomUser.objects.get(id=self.kwargs.get('pk'))
        serializer = ImageSerializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs.get("pk"))
        serializer = ImageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        image = get_object_or_404(CustomUser, id=self.kwargs.get("pk"))
        image.delete()
        return Response({"status": "success", "data": "Image Deleted"})


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


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleLinkUp(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookLinkUp(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuthAdapter
    serializer_class = TwitterLoginSerializer


class TwitterLinkUp(SocialConnectView):
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter
