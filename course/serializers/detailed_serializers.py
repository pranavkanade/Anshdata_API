from rest_framework.serializers import ModelSerializer
from core.models import Course, Unit, Lesson

from user_profile.serializer import UserSerializer

from course.serializers.serializers import UnitSerializer, LessonSerializer, AssignmentSerializer, CourseSerializer
from course.serializers.id_serializers import CourseIdSerializer, UnitIdSerializer
from course.serializers.util_serializers import AssignmentListSerializer


# All of the following are only used for read only purpose


class DetailedCourseSerializer(ModelSerializer):
    """
    This class is responsible for serializing the Course model
    """
    units = UnitSerializer(many=True, read_only=True)
    author = UserSerializer(many=False, read_only=True)

    # NOTE: Not making any relation with the assignments - Whenever added only should show
    # the course level assignments
    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'units')
        read_only_fields = ('author', 'units')
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['num_of_enrollments'] = instance.students.count()
        return response


class DetailedUnitSerializer(ModelSerializer):
    course = CourseIdSerializer(many=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    # NOTE: Not making any relation with the assignments - Whenever added only should show
    # the Unit level assignments
    class Meta:
        model = Unit
        fields = ('id', 'title', 'course', 'lessons')
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['course'] = CourseSerializer(instance.course).data['id']
        return response


class DetailedLessonSerializer(ModelSerializer):
    unit = UnitIdSerializer(many=False, read_only=True)
    assignments = AssignmentListSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'unit', 'assignments')
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['unit'] = UnitSerializer(instance.unit).data['id']
        return response


class DetailedAssignmentSerializer(AssignmentSerializer):
    # NOTE: We can get everything from AssignmentSerializer itself
    pass
