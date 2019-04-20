from rest_framework.serializers import ModelSerializer
from core.models import Course, Module, Assignment, Lesson


class CourseSerializer(ModelSerializer):
    """
    For creating the course
    """
    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'subject',
            'category',
            'is_published',
            'credit_points',
            'description'
        )
        read_only_fields = ('id', 'author', )
