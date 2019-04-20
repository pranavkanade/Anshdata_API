from rest_framework.serializers import ModelSerializer

from core.models import Category


class CategorySerializer(ModelSerializer):
    """
    Class to create and list of the categories
    """
    class Meta:
        model = Category
        fields = ('id', 'title', 'wiki')
        read_only = ('id', )
