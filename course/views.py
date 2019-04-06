from core.models import Course, Unit, Assignment, Lesson

from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from course.serializers.serializers import CourseSerializer, UnitSerializer, \
    AssignmentSerializer, LessonSerializer
from course.serializers.util_serializers import CourseEnrollSerializer

from rest_framework.response import Response


class CoursesListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UnitCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer


class UnitListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.filter(course=self.kwargs['crs_id'])


class LessonsCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonSerializer


class LessonsListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(unit=self.kwargs['unt_id'])


class AssignmentsCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AssignmentsListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        if 'unt_id' in self.kwargs.keys():
            if 'lsn_id' in self.kwargs.keys():
                return Assignment.objects.filter(
                    course=self.kwargs['crs_id'],
                    unit=self.kwargs['unt_id'],
                    lesson=self.kwargs['lsn']
                )
            else:
                return Assignment.objects.filter(
                    course=self.kwargs['crs_id'],
                    unit=self.kwargs['unt_id']
                )
        else:
            return Assignment.objects.filter(course=self.kwargs['crs_id'])


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
            raise PermissionDenied(detail="Users are not allowed to enroll in their own course")
        if did_update:
            payload = {
                'students': course_obj.students,
                'num_of_enrollments': course_obj.num_of_enrollments+1
            }
            return self.partial_update(request, payload)
        else:
            return Response({
                "details": "Already Enrolled"
            })
