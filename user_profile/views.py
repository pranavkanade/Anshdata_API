from django.contrib.auth import get_user_model

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from user_profile.serializer import \
    UserSerializer


class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


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
        print("[perform_create] : UserCreateView")
        serializer.save()


class UserGetView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.id)


class ListUserEnrolledCoursesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = UserCoursesEnrolledSerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.id)
