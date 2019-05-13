from django.urls import path
from course.views import EnrollInCourse,\
    CoursesListCreateView, CourseRetrieveUpdateDeleteView,\
    ModulesListCreateView, ModuleRetrieveUpdateDeleteView, ModulesMinListView,\
    LessonListCreateView, LessonRetrieveUpdateDeleteView,\
    AssignmentListCreateView, AssignmentRetrieveUpdateDeleteView,\
    DraftedCoursesCommunityListView, DraftedCoursesSelfListView,\
    EnrolledCoursesList, EnrollmentRetrieveView


app_name = 'course'

urlpatterns = [
    path('',
         CoursesListCreateView.as_view(),
         name='create_list_course'),
    path('enrolled/',
         EnrolledCoursesList.as_view(),
         name='enrolled_course_list'),
    path('enrolledin/<int:crs_id>/',
         EnrollmentRetrieveView.as_view(),
         name='is_enrolled_in_course'),
    path('drafts/comm/',
         DraftedCoursesCommunityListView.as_view(),
         name='list_unpublished_courses_by_community'),
    path('drafts/me/',
         DraftedCoursesSelfListView.as_view(),
         name='list_unpublished_courses_by_current_user'),
    path('<int:pk>/',
         CourseRetrieveUpdateDeleteView.as_view(),
         name='course_get_update_delete'),
    path('enroll/',
         EnrollInCourse.as_view(),
         name='enroll'),
    path('mod/',
         ModulesListCreateView.as_view(),
         name='create_module'),
    path('mod/<int:pk>/',
         ModuleRetrieveUpdateDeleteView.as_view(),
         name='module_get_update_delete'),
    path('<int:crs_id>/mod/',
         ModulesListCreateView.as_view(),
         name='list_modules_in_a_course'),
    path('<int:crs_id>/min/mod/',
         ModulesMinListView.as_view(),
         name='list_min_info_abt_modules'),
    path('lsn/',
         LessonListCreateView.as_view(),
         name='create_lesson'),
    path('lsn/<int:pk>/',
         LessonRetrieveUpdateDeleteView.as_view(),
         name='lesson_get_update_delete'),
    path('<int:mod_id>/lsn/',
         LessonListCreateView.as_view(),
         name='list_lessons_in_a_module'),
    path('ex/',
         AssignmentListCreateView.as_view(),
         name='create_assignment'),
    path('ex/<int:pk>/',
         AssignmentRetrieveUpdateDeleteView.as_view(),
         name='assignment_get_update_delete'),
    path('<int:crs_id>/ex/',
         AssignmentListCreateView.as_view(),
         name='list_assignments_crs'),
    path('mod/<int:mod_id>/ex/',
         AssignmentListCreateView.as_view(),
         name='list_assignments_mod'),
    path('lsn/<int:lsn_id>/ex/',
         AssignmentListCreateView.as_view(),
         name='list_assignments_lsn'),
]
