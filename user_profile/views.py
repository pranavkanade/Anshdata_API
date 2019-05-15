from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from user_profile.serializer import \
    UserSerializer, UserDetailedSerializer

from core.models.user import User
from core.models.profile import Profile, Social


class UserRetrieveView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailedSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['usr_name'])


class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_serializer_class(self, *args, **kwargs):
        print("[get_serializer_class] : UserCreateView")
        return UserSerializer

    def post(self, request, *args, **kwargs):
        print("[post] : UserCreateView")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        social_payload = dict()
        social = Social.objects.create(**social_payload)
        profile_payload = dict()
        profile = Profile.objects.create(**profile_payload)
        serializer.save(profile=profile, social=social)
