from rest_framework.serializers import ModelSerializer

from core.models import Feedback


class FeedbackSerializer(ModelSerializer):
    """
    Class to create and list of the categories
    """
    class Meta:
        model = Feedback
        fields = "__all__"
