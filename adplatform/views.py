from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from adplatform.serializers.category import CategorySerializer
from core.models import Category


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CategoryListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
