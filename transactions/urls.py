from django.urls import path

from .views import transaction_view, transaction_statistics


urlpatterns = [
    path("list/", transaction_view, name="transaction_list"),
    path("statistics/<time_period>/", transaction_statistics, name="transaction_statistics"),
]
