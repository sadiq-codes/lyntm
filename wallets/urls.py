from django.urls import path
from .views import set_wallet_pin, verify_wallet_pin, WalletDetailView, \
    transfer_funds, request_funds, RequestedFunds, accept_requested_funds, QRCodeView

urlpatterns = [
    path('set-pin/', set_wallet_pin, name="set_pin"),
    path('verify/', verify_wallet_pin, name="verify_pin"),
    path('<int:pk>/', WalletDetailView.as_view(), name="wallet_detail"),
    path('transfer/', transfer_funds, name="transfer_funds"),
    path('request/', request_funds, name="request_funds"),
    path('request/list/', RequestedFunds.as_view(), name="request_list"),
    path('request/accept/<int:pk>/', accept_requested_funds, name="accept_requested_funds"),
    path('qrcode/<account_number>', QRCodeView.as_view(), name="transaction_qrcode"),
]