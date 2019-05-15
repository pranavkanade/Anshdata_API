from django.urls import path
from user_profile.views import UserCreateView, UserRetrieveView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


app_name = 'user_profile'

urlpatterns = [
    path('u/<str:usr_name>/', UserRetrieveView.as_view(), name='list-users'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh/', refresh_jwt_token, name='refresh')
]
