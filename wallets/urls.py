from django.urls import path
from .views import set_wallet_pin, verify_wallet_pin, WalletDetailView, transfer

urlpatterns = [
    path('set-pin/', set_wallet_pin, name="set_pin"),
    path('verify/', verify_wallet_pin, name="verify_pin"),
    path('<int:pk>/', WalletDetailView.as_view(), name="wallet_detail"),
    path('transfer/', transfer, name="transfer_funds"),
]