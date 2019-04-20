# from rest_framework.serializers import ModelSerializer
# from core.models import Course, Module, Assignment, Lesson
#
#
# class CourseSerializer(ModelSerializer):
#     """
#     This class is responsible for serializing the Course model
#     """
#     class Meta:
#         model = Course
#         fields = ('id', 'author', 'title', 'students')
#         read_only_fields = ('id', 'author', )
#
#
# class UnitSerializer(ModelSerializer):
#     """
#     This class serializes Unit model
#     """
#     class Meta:
#         model = Unit
#         fields = ('id', 'title', 'course')
#         read_only_fields = ('id', )
#
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         # TODO: Change following serializer to get more or less attributes of course object
#         response['course'] = CourseSerializer(instance.course).data['id']
#         return response
#
#
# class LessonSerializer(ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ('id', 'title', 'unit')
#         read_only_fields = ('id',)
#
#
# class AssignmentSerializer(ModelSerializer):
#     """
#     This class serializes Unit model
#     """
#     class Meta:
#         model = Assignment
#         fields = ('id', 'title', 'author', 'lesson', 'unit', 'course')
#         read_only_fields = ('id', 'author',)
#
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         # TODO
#         response['unit'] = UnitSerializer(instance.unit).data['id']
#         response['lesson'] = LessonSerializer(instance.lesson).data['id']
#         response['course'] = CourseSerializer(instance.course).data['id']
#         return response
