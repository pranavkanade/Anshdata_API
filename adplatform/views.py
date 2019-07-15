from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny

from adplatform.serializers.category import CategorySerializer
from adplatform.serializers.tag import TagSerializer
from adplatform.serializers.feedback import FeedbackSerializer
from core.models import Category
from core.models import Tag, Feedback


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CategoryListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TagListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class FeedbackCreateView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class FeedbackListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
