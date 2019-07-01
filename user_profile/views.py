from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_auth.registration.views import RegisterView

from user_profile.serializer import \
    UserSerializer, UserDetailedSerializer,\
    ProfileSerializer, SocialSerializer, \
    UserRegisterSerializer

from core.models.user import User
from core.models.profile import Profile, Social


class UserRetrieveView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailedSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['usr_name'])


class CurrentUserRetrieveView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)


class UserCreateView(RegisterView):
    serializer_class = UserRegisterSerializer


class SocialRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SocialSerializer

    def get_queryset(self):
        return Social.objects.filter(pk=self.kwargs['pk'])


class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(pk=self.kwargs['pk'])
