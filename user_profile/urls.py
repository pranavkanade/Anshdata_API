from django.urls import path
from user_profile.views import (
    UserCreateView, UserRetrieveView,
    ProfileRetrieveUpdateView, SocialRetrieveUpdateView,

)
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView
)
from rest_framework_jwt.views import refresh_jwt_token


app_name = 'user_profile'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('me/', UserDetailsView.as_view(), name='rest_user_details'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(),
         name='retrieve_update_profile'),
    path('social/<int:pk>/', SocialRetrieveUpdateView.as_view(),
         name='retrieve_update_social'),
    path('<str:usr_name>/', UserRetrieveView.as_view(), name='list-users')
]
