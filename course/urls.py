from django.urls import path
from course.views import CoursesListCreateView, UnitListView, \
    AssignmentsListView, EnrollInCourse, LessonsCreateView, \
    UnitCreateView, LessonsListView, AssignmentsCreateView

app_name = 'course'

urlpatterns = [
    path('', CoursesListCreateView.as_view(), name='create_list_course'),
    path('<int:pk>/enroll/', EnrollInCourse.as_view(), name='enroll'),
    path('unt/', UnitCreateView.as_view(), name='create_unit'),
    path('<int:crs_id>/unt/', UnitListView.as_view(), name='list_unit'),
    path('lsn/', LessonsCreateView.as_view(), name='create_lesson'),
    path('<int:unt_id>/lsn/', LessonsListView.as_view(), name='list_lesson'),
    path('ex/', AssignmentsCreateView.as_view(), name='create_assignment'),
    path('<int:crs_id>/ex/', AssignmentsListView.as_view(), name='list_assignments_crs'),
    path('<int:crs_id>/<int:unt_id>/ex/', AssignmentsListView.as_view(), name='list_assignments_crs_unt'),
    path('<int:crs_id>/<int:unt_id>/<int:lsn_id>/ex/',
         AssignmentsListView.as_view(),
         name='list_assignments_crs_unt_lsn'),
]
