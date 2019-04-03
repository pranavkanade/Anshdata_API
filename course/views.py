from core.models import Course, Unit, Assignment

from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from course.serializers.serializer import CourseSerializer, UnitSerializer, AssignmentSerializer
from course.serializers.detail_serializer import CourseDetailUserSerializer, CourseEnrollSerializer

from rest_framework.response import Response


class CoursesList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseDetailUserSerializer
    queryset = Course.objects.all()


class CoursesListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # NOTE: Following function needs to be added here to pass on the
    # author of the course.
    # TODO: @here check if the user is producer else raise error
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UnitsListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()


class AssignmentsListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()


class EnrollInCourse(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseEnrollSerializer
    queryset = Course.objects.all()

    def patch(self, request, *args, **kwargs):
        course_obj = get_object_or_404(Course, pk=kwargs['pk'])
        did_update = False
        # this means the user is not creator
        if course_obj.author.id != request.user.id:
            if request.user not in course_obj.students.all():
                # If user has already disliked the post. toggle the person's dislike
                course_obj.students.add(request.user)
                did_update = True
        else:
            raise PermissionDenied(detail="Users are not allowed to dislike their own post")
        if did_update:
            payload = {
                'students': course_obj.students
            }
            return self.partial_update(request, payload)
        else:
            return Response({
                "details": "Already Enrolled"
            })
