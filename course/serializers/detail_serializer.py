from rest_framework.serializers import ModelSerializer
from core.models import Course

from user_profile.serializer import UserSerializer

from course.serializers.serializer import CourseSerializer, UnitSerializer


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


class CourseEnrollSerializer(CourseSerializer):
    students = UserSerializer(many=True, read_only=False)
