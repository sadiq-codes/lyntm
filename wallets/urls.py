from django.urls import path
from .views import set_wallet_pin, verify_wallet_pin

urlpatterns = [
    path('set-pin/', set_wallet_pin,),
    path('verify/', verify_wallet_pin),
]