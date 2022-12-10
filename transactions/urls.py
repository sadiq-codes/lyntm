from django.urls import path

from .views import transaction_statistics, TransactionView


urlpatterns = [
    path("list/", TransactionView.as_view(), name="transaction_list"),
    path("statistics/<time_period>/", transaction_statistics, name="transaction_statistics"),
]
