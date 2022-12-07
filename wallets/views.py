from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# Create your views here.

from transactions.serializers import TransactionSerializer
from .models import Wallet
from .serializers import PinSerializer, WalletSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def set_wallet_pin(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = PinSerializer(data=request.data)
    if serializer.is_valid():
        wallet.set_pin(serializer.data.get("pin"))
        return Response({"status": "success", "message": "Pin set successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "failed", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def verify_wallet_pin(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = PinSerializer(data=request.data)
    if serializer.is_valid():
        if wallet.check_pin(serializer.data.get("pin")):
            return Response({"status": "success", "message": "Pin verified"}, status=status.HTTP_200_OK)
        return Response({"status": "failed", "message": "incorrect wallet pin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "failed", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def transfer(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.data)
        receiver = serializer.data.get("receiver")
        amount = serializer.data.get("amount")
        notes = serializer.data.get("notes")
        category = serializer.data.get("transaction_category")
        schedule = serializer.data.get("schedule")
        pin = serializer.data.get("pin")
        receiver = get_object_or_404(Wallet, user_id=receiver)
        wallet.transfer(wallet, receiver, amount, category, notes,  pin, schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

