from core.models import (Course, Module, Assignment, Lesson,
                         CourseProgress, LessonCompleted, AssignmentCompleted,
                         Category)
from core.models import User

from rest_framework.generics import (
    ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView,
    UpdateAPIView)
from rest_framework.permissions import (
    IsAuthenticated, BasePermission, SAFE_METHODS, AllowAny)
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.response import Response

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

from course.serializers import creation, listing, detailed
from pprint import pprint


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CoursesListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = listing.CourseSerializer
    # queryset = Course.objects.all()

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            return Course.objects.filter(is_published=True)

        users_to_include = User.objects.exclude(pk=self.request.user.id)
        return (
            Course.objects.filter(
                is_published=True,
                author__in=users_to_include
            ).difference(Course.objects.filter(
                enrollments__candidate=self.request.user)))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        self.serializer_class = detailed.CourseSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = creation.CourseSerializer
        return self.create(request, *args, **kwargs)


class PublishCourse(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = creation.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to publish the course.", code=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(
            instance, data={'is_published': True}, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class DraftCourse(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = creation.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to open the course for modification.", code=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(
            instance, data={'is_published': False}, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PublishedCoursesListByUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['usr_id'])
        return Course.objects.filter(is_published=True, author=user)


class PopularCouseListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        _q = Course.objects
        return _q.filter(is_published=True).order_by('-students_count')[:10]


class EnrolledCoursesList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(enrollments__candidate=self.request.user)


class EnrollmentRetrieveView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = listing.CourseProgressSerializer

    def get_queryset(self):
        return CourseProgress.objects.filter(candidate=self.request.user, course=self.kwargs['crs_id'])


# List the unpublished courses
class DraftedCoursesCommunityListView(ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        if self.request.user == AnonymousUser:
            return Course.objects.filter(is_published=False)
        users_to_include = User.objects.exclude(pk=self.request.user.id)
        return Course.objects.filter(is_published=False, author__in=users_to_include)


class DraftedCoursesSelfListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = detailed.CourseSerializer

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


class CourseRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs['pk'])

    def get_serializer(self, *args, **kwargs):

        if self.request.method == "PATCH":
            serializer_class = creation.CourseSerializer
            print("PATCH method called !")
        else:
            serializer_class = self.get_serializer_class()

        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to update.", code=status.HTTP_401_UNAUTHORIZED)

        courseId = self.kwargs['pk']
        if 'course' in request.data.keys():
            courseId = request.data['course']
        course = get_object_or_404(Course, pk=courseId)
        if course.is_published:
            raise PermissionDenied(
                detail=("Sorry, the course is not open for modification."
                        " Please open the course for modification first."),
                code=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to delete.", code=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModuleRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.ModuleSerializer

    def get_queryset(self):
        return Module.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to update.", code=status.HTTP_401_UNAUTHORIZED)

        courseId = instance.course.id
        if 'course' in request.data.keys():
            courseId = request.data['course']
        course = get_object_or_404(Course, pk=courseId)
        if course.is_published:
            raise PermissionDenied(
                detail=("Sorry, the course is not open for modification."
                        " Please open the course for modification first."),
                code=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to delete.", code=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to update.", code=status.HTTP_401_UNAUTHORIZED)

        courseId = instance.module.course.id
        if 'course' in request.data.keys():
            courseId = request.data['course']
        course = get_object_or_404(Course, pk=courseId)
        if course.is_published:
            raise PermissionDenied(
                detail=("Sorry, the course is not open for modification."
                        " Please open the course for modification first."),
                code=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to delete.", code=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignmentRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = detailed.AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to update.", code=status.HTTP_401_UNAUTHORIZED)
        courseId = instance.course.id
        if 'course' in request.data.keys():
            courseId = request.data['course']
        course = get_object_or_404(Course, pk=courseId)
        if course.is_published:
            raise PermissionDenied(
                detail=("Sorry, the course is not open for modification."
                        " Please open the course for modification first."),
                code=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id != request.user.id:
            raise PermissionDenied(
                detail="Sorry, only author has the permission to delete.", code=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# NOTE: For now I am creating this to see what is inside the enrollment model
class EnrollInCourse(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = creation.CourseProgressSerializer
    queryset = CourseProgress.objects.all()

    def create(self, request, *args, **kwargs):
        course = request.data['course']
        course = get_object_or_404(Course, pk=course)
        candidate = request.user
        pg = CourseProgress.objects.filter(course=course, candidate=candidate)
        pprint(pg)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)


class RegisterCourseProgressView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = creation.CourseProgressSerializer
    queryset = CourseProgress.objects.all()

    def get_queryset(self):
        return CourseProgress.objects.filter(pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MarkLessonCompleteView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = creation.LessonCompletedSerializer
    queryset = LessonCompleted.objects.all()

    def get_queryset(self):
        if self.request.method == "GET":
            return LessonCompleted.objects.filter(
                enrollment__candidate=self.request.user
            )
        else:
            return LessonCompleted.objects.all()


class MarkAssignmentCompleteView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = creation.AssignmentCompletedSerializer
    queryset = AssignmentCompleted.objects.all()

    def get_queryset(self):
        if self.request.method == "GET":
            return AssignmentCompleted.objects.filter(
                enrollment__candidate=self.request.user
            )
        else:
            return AssignmentCompleted.objects.all()
