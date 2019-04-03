from rest_framework.serializers import ModelSerializer
from core.models import Course, Unit, Assignment


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


# NOTE: Get id only
class CourseIDSerializer(ModelSerializer):
    """
    This class is responsible for serializing the Course model
    """
    class Meta:
        model = Course
        fields = ('id',)

