import qrcode
from django.http import HttpResponse
from django.views import View
from qrcode import QRCode
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from .models import Wallet
from .serializers import PinSerializer, WalletSerializer, DepositSerializer


# Create your views here.


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def set_wallet_pin(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = PinSerializer(data=request.data)
    if serializer.is_valid():
        wallet.set_pin(serializer.data.get("pin"))
        return Response({"status": "success", "data": "Pin set successfully"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def verify_wallet_pin(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = PinSerializer(data=request.data)
    if serializer.is_valid():
        if wallet.check_pin(serializer.data.get("pin")):
            return Response({"data": "Pin verified"}, status=status.HTTP_200_OK)
        return Response({"data": "incorrect wallet pin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def withdraw_funds(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
        data = get_data(serializer)
        wallet.withdraw(wallet, data.get('amount'),
                        data.get('category'), data.get('notes'), )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def deposit_funds(request):
    wallet = Wallet.objects.get(user=request.user)
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
        data = get_data(serializer)

        wallet.deposit(wallet, data.get('amount'),
                       data.get('category'), data.get('notes'), )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {"amount": 5000, "transaction_category": "", "notes": "Thank you"}


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def transfer_funds(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        data = get_data(serializer)
        wallet.transfer(wallet, data.get('receiver'), data.get('amount'),
                        data.get('category'), data.get('notes'), data.get('schedule'))
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def request_funds(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        data = get_data(serializer)
        wallet.request_payment(wallet, data.get('receiver'), data.get('amount'),
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
    return Response({"data": "Funds Transferred"}, status=status.HTTP_200_OK)


class QRCodeView(View):

    def get(self, request, **kwargs):
        # Create a QR code object
        qr = QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(kwargs.get("account_number"))
        qr.make(fit=True)
        img = qr.make_image(fill_color="blue", back_color="white")
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")

        return response
