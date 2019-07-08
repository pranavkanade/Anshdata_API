from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from core.models import (
    Course, Module, Assignment, Lesson,
    CourseProgress, LessonCompleted, AssignmentCompleted, Tag)


class CourseSerializer(ModelSerializer):
    """
    For creating the course
    """
    tagged_to = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'subject',
            'tagged_to',
            'category',
            'is_published',
            'credit_points',
            'description'
        )
        read_only_fields = ('id', 'author',)

    # TODO: Add function to_representation so that it returns name of the category


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = (
            'id',
            'author',
            'title',
            'description',
            'course',
            'reference'
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
            'module'
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


class CourseProgressSerializer(ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = (
            'id',
            'candidate',
            'course',
            'current_lesson',
            'current_assignment'
        )
        read_only_fields = ('id', 'candidate', )


class LessonCompletedSerializer(ModelSerializer):
    class Meta:
        model = LessonCompleted
        fields = '__all__'


class AssignmentCompletedSerializer(ModelSerializer):
    class Meta:
        model = AssignmentCompleted
        fields = '__all__'
