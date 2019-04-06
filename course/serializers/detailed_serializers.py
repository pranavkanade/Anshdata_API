from rest_framework.serializers import ModelSerializer
from core.models import Course, Unit, Lesson

from user_profile.serializer import UserSerializer

from course.serializers.serializers import UnitSerializer, LessonSerializer, AssignmentSerializer
from course.serializers.id_serializers import CourseIdSerializer, UnitIdSerializer
from course.serializers.util_serializers import AssignmentListSerializer


# All of the following are only used for read only purpose


class DetailedCourseSerializer(ModelSerializer):
    """
    This class is responsible for serializing the Course model
    """
    units = UnitSerializer(many=True, read_only=True, source='units')
    author = UserSerializer(many=False, read_only=True)

    # NOTE: Not making any relation with the assignments - Whenever added only should show
    # the course level assignments
    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'units', 'num_of_enrollments')
        read_only_fields = ('author', 'units')
        depth = 1


class DetailedUnitSerializer(ModelSerializer):
    course = CourseIdSerializer(many=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source='lessons')

    # NOTE: Not making any relation with the assignments - Whenever added only should show
    # the Unit level assignments
    class Meta:
        model = Unit
        fields = ('id', 'title', 'course', 'lessons')
        depth = 1


class DetailedLessonSerializer(ModelSerializer):
    unit = UnitIdSerializer(many=False, read_only=True)
    assignments = AssignmentListSerializer(many=True, read_only=True, source='assignments')

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'unit', 'assignments')
        depth = 1


class DetailedAssignmentSerializer(AssignmentSerializer):
    # NOTE: We can get everything from AssignmentSerializer itself
    pass
