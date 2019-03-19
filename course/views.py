from core.models import Course, Unit, Assignment

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from course.serializer import CourseSerializer, UnitSerializer, AssignmentSerializer, CourseDetailUserSerializer


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
