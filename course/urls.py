from django.urls import path
from course.views import CoursesListCreateView, UnitsListCreateView, AssignmentsListCreateView, EnrollInCourse

app_name = 'course'

urlpatterns = [
    path('', CoursesListCreateView.as_view(), name='course_list_create'),
    path('<int:pk>/enroll/', EnrollInCourse.as_view(), name='enroll'),
    path('lsn/', UnitsListCreateView.as_view(), name='unit_list_create'),               # lessons
    path('ex/', AssignmentsListCreateView.as_view(), name='assignment_list_create')     # exercise
]
