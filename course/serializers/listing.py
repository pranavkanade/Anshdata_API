from rest_framework.serializers import ModelSerializer
from core.models import Course, Module, Assignment, Lesson, CourseProgress, LessonCompleted, AssignmentCompleted
from user_profile.serializer import UserSerializer
from adplatform.serializers import CategorySerializer


class CourseSerializer(ModelSerializer):
    """
    For creating the course
    """
    author = UserSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'subject',
            'category',
            'tagged_to',
            'is_published',
            'credit_points',
            'description',
            'modules',
            'assignments'
        )
        read_only_fields = ('id', 'author', )


class ModuleSerializer(ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

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
        read_only_fields = ('id', 'author',)


class LessonSerializer(ModuleSerializer):
    author = UserSerializer(many=False, read_only=True)

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
        read_only_fields = ('id', 'author',)


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


# Min serializer

class AssignmentSerializerMin(ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            'id',
            'title',
            'credit_points',
        )
        read_only_fields = ('id', )


class LessonSerializerMin(ModelSerializer):
    """
    For listing the lessons min
    """
    class Meta:
        model = Lesson
        fields = (
            'id',
            'title'
        )


class ModuleSerializerMin(ModelSerializer):
    """
    For Listing the module min
    """
    lessons = LessonSerializerMin(many=True, read_only=True)
    assignments = AssignmentSerializerMin(many=True, read_only=True)

    class Meta:
        model = Module
        fields = (
            'id',
            'title',
            'description',
            'lessons',
            'assignments'
        )
        read_only_fields = ('id',)


class LessonCompletedSerializer(ModelSerializer):
    class Meta:
        model = LessonCompleted
        fields = '__all__'


class AssignmentCompletedSerializer(ModelSerializer):
    class Meta:
        model = AssignmentCompleted
        fields = '__all__'


class CourseProgressSerializer(ModelSerializer):
    completed_lessons = LessonCompletedSerializer(many=True, read_only=True)
    completed_assignments = AssignmentCompletedSerializer(
        many=True, read_only=True)

    class Meta:
        model = CourseProgress
        fields = (
            'id',
            'candidate',
            'course',
            'current_lesson',
            'current_assignment',
            'completed_lessons',
            'completed_assignments'
        )
        read_only_fields = ('id', 'candidate', )
