from django.shortcuts import render
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# Create your views here.

from transactions.serializers import TransactionSerializer
from transactions.models import Transaction
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


def get_data(serializer):
    receiver = serializer.data.get("receiver")
    amount = serializer.data.get("amount")
    notes = serializer.data.get("notes")
    category = serializer.data.get("transaction_category")
    schedule = serializer.data.get("schedule")
    receiver = get_object_or_404(Wallet, id=receiver)
    return dict(receiver=receiver, amount=amount, category=category, notes=notes, schedule=schedule)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def transfer_funds(request):
    sender = get_object_or_404(Wallet, user=request.user)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        data = get_data(serializer)
        sender.transfer(sender, data.get('receiver'), data.get('amount'),
                        data.get('category'), data.get('notes'), data.get('schedule'))
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def request_funds(request):
    sender = get_object_or_404(Wallet, user=request.user)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        data = get_data(serializer)
        sender.request_payment(sender, data.get('receiver'), data.get('amount'),
                               data.get('category'), data.get('notes'))
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestedFunds(generics.ListAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        wallet = get_object_or_404(Wallet, user=self.request.user)
        return Transaction.objects.filter(receiver=wallet,
                                          transaction_status="REQUESTED").order_by("-transaction_date")


@api_view(["POST"])
def accept_requested_funds(request, pk):
    wallet = get_object_or_404(Wallet, user=request.user)
    wallet.accept_request(pk)
    return Response({"status": "success", "message": "Funds Transferred"}, status=status.HTTP_200_OK)

