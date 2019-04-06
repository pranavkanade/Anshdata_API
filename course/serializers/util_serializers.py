from rest_framework.serializers import ModelSerializer
from user_profile.serializer import UserSerializer
from course.serializers.serializers import CourseSerializer

from core.models import Assignment


class CourseEnrollSerializer(CourseSerializer):
    students = UserSerializer(many=True, read_only=False)


class AssignmentListSerializer(ModelSerializer):
    """
    This class serializes Unit model
    """
    class Meta:
        model = Assignment
        fields = ('id', 'title', 'author', 'lesson')
        read_only_fields = ('id', 'author',)
