from django.urls import path
from user_profile.views import UserCreateView, UserRetrieveView,\
    ProfileRetrieveUpdateView, SocialRetrieveUpdateView,\
    CurrentUserRetrieveView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


app_name = 'user_profile'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('me/', CurrentUserRetrieveView.as_view(), name='get_current_user'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(), name='retrieve_update_profile'),
    path('social/<int:pk>/', SocialRetrieveUpdateView.as_view(), name='retrieve_update_social'),
    path('<str:usr_name>/', UserRetrieveView.as_view(), name='list-users')
]
