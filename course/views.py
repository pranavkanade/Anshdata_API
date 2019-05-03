from core.models import Course, Module, Assignment, Lesson, CourseEnrollment

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, AllowAny
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed

from course.serializers import creation, listing, detailed


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CoursesListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = listing.CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        self.serializer_class = listing.CourseSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = creation.CourseSerializer
        return self.create(request, *args, **kwargs)


class CourseRetrieveView(RetrieveAPIView):
    permission_classes = (ReadOnly, )
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs['pk'])


# List the unpublished courses
class SavedCoursesListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = listing.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(is_published=False, author=self.request.user)


class ModulesListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = listing.ModuleSerializer

    # The following function will list out all the modules of a course
    # with given crs_id
    def get_queryset(self):
        return Module.objects.filter(course=self.kwargs['crs_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        if 'crs_id' not in self.kwargs.keys():
            raise MethodNotAllowed("GET",
                                   detail="Sorry, GET method is not allowed on the address you are trying to access.",
                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serializer_class = listing.ModuleSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'crs_id' in self.kwargs.keys():
            raise MethodNotAllowed("POST",
                                   detail="Sorry, POST method is not allowed on the address you are trying to access.",
                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serializer_class = creation.ModuleSerializer
        return self.create(request, *args, **kwargs)


class ModulesMinListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = listing.ModuleSerializerMin

    def get_queryset(self):
        return reversed(Module.objects.filter(course=self.kwargs['crs_id']))


class ModuleRetrieveView(RetrieveAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = detailed.ModuleSerializer

    def get_queryset(self):
        return Module.objects.filter(pk=self.kwargs['pk'])


class LessonListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly, )
    serializer_class = listing.LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(module=self.kwargs['mod_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        if 'mod_id' not in self.kwargs.keys():
            raise MethodNotAllowed("GET",
                                   detail="Sorry, GET method is not allowed on the address you are trying to access.",
                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serializer_class = listing.LessonSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'mod_id' in self.kwargs.keys():
            raise MethodNotAllowed("POST",
                                   detail="Sorry, POST method is not allowed on the address you are trying to access.",
                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serializer_class = creation.LessonSerializer
        return self.create(request, *args, **kwargs)


class LessonRetrieveView(RetrieveAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = detailed.LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(pk=self.kwargs['pk'])


class AssignmentListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly, )
    serializer_class = listing.AssignmentSerializer

    def get_queryset(self):
        if 'crs_id' in self.kwargs.keys():
            return Assignment.objects.filter(course=self.kwargs['crs_id'])
        elif 'mod_id' in self.kwargs.keys():
            return Assignment.objects.filter(module=self.kwargs['mod_id'])
        elif 'lsn_id' in self.kwargs.keys():
            return Assignment.objects.filter(lesson=self.kwargs['lsn_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        if len(self.kwargs.keys()) == 0:
            raise MethodNotAllowed("GET",
                                   detail="Sorry, GET method is not allowed on the address you are trying to access.",
                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serializer_class = listing.AssignmentSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if len(self.kwargs.keys()) > 0:
            raise MethodNotAllowed("POST",
                                   detail="Sorry, POST method is not allowed on the address you are trying to access.",
                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serializer_class = creation.AssignmentSerializer
        return self.create(request, *args, **kwargs)


class AssignmentRetrieveView(RetrieveAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = detailed.AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.filter(pk=self.kwargs['pk'])


# NOTE: For now I am creating this to see what is inside the enrollment model
class EnrollInCourse(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = creation.CourseEnrollSerializer
    queryset = CourseEnrollment.objects.all()

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)
