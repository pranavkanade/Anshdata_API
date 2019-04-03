from django.contrib.auth import get_user_model

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from user_profile.serializer import \
    UserSerializer, \
    ProducerDetailedSerializer, \
    ConsumerDetailedSerializer, \
    UserCoursesEnrolledSerializer


class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_serializer_class(self, *args, **kwargs):
        print("[get_serializer_class] : UserCreateView")
        is_producer = False
        if 'is_producer' in self.request.data.keys():
            is_producer = self.request.data['is_producer']
        if is_producer:
            return ProducerDetailedSerializer
        else:
            return ConsumerDetailedSerializer

    def post(self, request, *args, **kwargs):
        print("[post] : UserCreateView")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("[perform_create] : UserCreateView")
        is_producer = False
        if 'is_producer' in self.request.data.keys():
            is_producer = self.request.data['is_producer']
        generic_user = get_user_model().objects.create_user(username=self.request.data['username'],
                                                            email=self.request.data['email'],
                                                            password=self.request.data["password"],
                                                            is_producer=is_producer)
        serializer.save(user=generic_user)


class UserGetView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.id)


class ListUserEnrolledCoursesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCoursesEnrolledSerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.id)
