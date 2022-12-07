from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# Create your views here.

from .serializers import TransactionSerializer
from .models import Transaction
from wallets.models import Wallet
from wallets.serializers import PinSerializer, WalletSerializer


# Create your views here.

class TransactionView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
