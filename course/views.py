from core.models import Course, Module, Assignment, Lesson, CourseEnrollment
from core.models import User

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, AllowAny
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.response import Response

from django.contrib.auth.models import AnonymousUser

from course.serializers import creation, listing, detailed


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CoursesListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = listing.CourseSerializer
    # queryset = Course.objects.all()

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        if self.request.user == AnonymousUser:
            return Course.objects.filter(is_published=True)

        print("test")
        users_to_include = User.objects.exclude(pk=self.request.user.id)
        return Course.objects.filter(
            is_published=True,
            author__in=users_to_include,
            enrollments__candidate__in=users_to_include)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        self.serializer_class = listing.CourseSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = creation.CourseSerializer
        return self.create(request, *args, **kwargs)


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


class RetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    # NOTE: copied following fuction from the lib as it is.
    # with small change - Added a condition to find if the
    # request is issued by the author itself or someone else.
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(instance.author.id)
        print(request.user.id)
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to update.", code=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to delete.", code=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseRetrieveUpdateDeleteView(RetrieveUpdateDestroyView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs['pk'])


class ModuleRetrieveUpdateDeleteView(RetrieveUpdateDestroyView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.ModuleSerializer

    def get_queryset(self):
        return Module.objects.filter(pk=self.kwargs['pk'])


class LessonRetrieveUpdateDeleteView(RetrieveUpdateDestroyView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(pk=self.kwargs['pk'])


class AssignmentRetrieveUpdateDeleteView(RetrieveUpdateDestroyView):
    permission_classes = (IsAuthenticated | ReadOnly,)
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
