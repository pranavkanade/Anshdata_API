from django.urls import path
from course.views import CoursesListCreateView, UnitsListCreateView, AssignmentsListCreateView, CoursesList

app_name = 'core'

urlpatterns = [
    path('', CoursesListCreateView.as_view(), name='course_list_create'),
    path('lsn/', UnitsListCreateView.as_view(), name='unit_list_create'),               # lessons
    path('ex/', AssignmentsListCreateView.as_view(), name='assignment_list_create')     # exercise
]
