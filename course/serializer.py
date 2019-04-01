from rest_framework.serializers import ModelSerializer
from core.models import Course, Unit, Assignment, Consumer

from user_profile.serializer import UserSerializer, ConsumerSerializer


class CourseSerializer(ModelSerializer):
    """
    This class is responsible for serializing the Course model
    """
    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'students')
        read_only_fields = ('author', )


class UnitSerializer(ModelSerializer):
    """
    This class serializes Unit model
    """
    class Meta:
        model = Unit
        fields = ('id', 'course', 'title')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # TODO: Change following serializer to get more or less attributes of course object
        response['course'] = CourseSerializer(instance.course).data
        return response


class AssignmentSerializer(ModelSerializer):
    """
    This class serializes Unit model
    """
    class Meta:
        model = Assignment
        fields = ('id', 'unit', 'title')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # TODO
        response['unit'] = UnitSerializer(instance.unit).data
        return response


# NOTE: Following classes can be used to extensive output depending on which class you are using
class CourseDetailUserSerializer(CourseSerializer):
    author = UserSerializer(many=False, read_only=True)
    students = UserSerializer(many=True, read_only=True)


class CourseDetailUserUnitSerializer(ModelSerializer):
    """
    This class is responsible for serializing the Course model
    """
    units = UnitSerializer(many=True, read_only=True)
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'author', 'title', 'units')
        read_only_fields = ('author', 'units')


# NOTE: Get id only
class CourseIDSerializer(ModelSerializer):
    """
    This class is responsible for serializing the Course model
    """
    class Meta:
        model = Course
        fields = ('id',)


class CourseEnrollSerializer(CourseSerializer):
    students = UserSerializer(many=True, read_only=False)
