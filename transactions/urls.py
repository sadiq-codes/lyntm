from django.urls import path

from .views import TransactionView

urlpatterns = [
    path("list/", TransactionView.as_view(), name="transaction_list")
]
