from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from adplatform.serializers.category import CategorySerializer
from core.models import Category


class CategoryListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
