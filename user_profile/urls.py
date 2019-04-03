from django.contrib import admin
from django.urls import path
from user_profile.views import UserCreateView, UserListView, UserGetView,\
    ListUserEnrolledCoursesView
from rest_framework_jwt.views import obtain_jwt_token


app_name = 'user_profile'

urlpatterns = [
    path('me/', UserGetView.as_view(), name='get-loggedin-user'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', obtain_jwt_token),
    path('all/', UserListView.as_view(), name='list-users'),
    path('enrolledin/', ListUserEnrolledCoursesView.as_view(), name="enrolledin-courses"),
]
