from django.shortcuts import render
from rest_framework import status, generics, viewsets
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
@api_view(["GET"])
def transaction_view(request):
    transactions = Transaction.objects.all()

    serializer = TransactionSerializer(transactions, many=True)

    response_data = serializer.data
    print(response_data)
    # for transaction in response_data:
    #     transaction['transaction_type'] = serializer.get_transaction_type(transaction)

    return Response(response_data)


class StatisticsView(generics.ListAPIView):
    serializer_class = TransactionSerializer


@api_view(["GET"])
def transaction_statistics(request, time_period):
    wallet = get_object_or_404(Wallet, user=request.user)

    # transactions = Transaction.get_statistics(wallet, time_period=time_period).all()
    transactions = wallet.get_statistics(time_period=time_period).all()
    return Response({"data": transactions}, status=status.HTTP_200_OK)
