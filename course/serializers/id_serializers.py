# from rest_framework.serializers import ModelSerializer
# from core.models import Course, Unit, Assignment, Lesson
#
#
# # NOTE: Get id only
# class CourseIdSerializer(ModelSerializer):
#     """
#     This class is responsible for serializing the Course model
#     """
#     class Meta:
#         model = Course
#         fields = ('id',)
#
#
# class UnitIdSerializer(ModelSerializer):
#     """
#     This class serializes Unit model
#     """
#     class Meta:
#         model = Unit
#         fields = ('id',)
#
#
# class LessonIdSerializer(ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ('id',)
#
#
# class AssignmentIdSerializer(ModelSerializer):
#     """
#     This class serializes Unit model
#     """
#     class Meta:
#         model = Assignment
#         fields = ('id',)
