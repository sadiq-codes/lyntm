from django.urls import path

from .views import UserList, UserDetail, ProfileImage, GoogleLogin, GoogleLinkUp, \
   TwitterLogin, TwitterLinkUp, FacebookLinkUp, FacebookLogin


urlpatterns = [
   path('users/', UserList.as_view()),
   path('users/<int:pk>/', UserDetail.as_view()),
   path('users/<int:pk>/image/', ProfileImage.as_view()),
   path('rest-auth/google/', GoogleLogin.as_view()),
   path('rest-auth/google/linkup/', GoogleLinkUp.as_view()),
   path('rest-auth/facebook/', FacebookLogin.as_view()),
   path('rest-auth/facebook/linkup/', FacebookLinkUp.as_view()),
   path('rest-auth/twitter/', TwitterLogin.as_view()),
   path('rest-auth/twitter/linkup', TwitterLinkUp.as_view())
]