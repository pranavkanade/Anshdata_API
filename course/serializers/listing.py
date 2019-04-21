from rest_framework.serializers import ModelSerializer
from core.models import Course, Module, Assignment, Lesson, CourseEnrollment


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
            'description',
            'modules',
            'assignments'
        )
        read_only_fields = ('id', 'author', )


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = (
            'id',
            'author',
            'title',
            'description',
            'course',
            'reference',
            'lessons',
            'assignments'
        )
        read_only_fields = ('id', 'author', )


class LessonSerializer(ModuleSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'author',
            'title',
            'description',
            'lecture',
            'module',
            'assignments'
        )
        read_only_fields = ('id', 'author', )


class AssignmentSerializer(ModuleSerializer):
    class Meta:
        model = Assignment
        fields = (
            'id',
            'author',
            'title',
            'instruction',
            'lesson',
            'module',
            'course',
            'credit_points',
            'reference'
        )
        read_only_fields = ('id', 'author', )