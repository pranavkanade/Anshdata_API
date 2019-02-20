from django.contrib import admin
from django.urls import path
from user_profile.views import UserCreateView, UserListView


app_name = 'user_profile'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('all/', UserListView.as_view(), name='list-users'),
]
