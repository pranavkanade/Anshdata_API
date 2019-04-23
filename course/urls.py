from django.urls import path
from course.views import EnrollInCourse,\
    CoursesListCreateView, CourseRetrieveView,\
    ModulesListCreateView, ModuleRetrieveView,\
    LessonListCreateView, LessonRetrieveView,\
    AssignmentListCreateView, AssignmentRetrieveView,\
    SavedCoursesListView


app_name = 'course'

urlpatterns = [
    path('', CoursesListCreateView.as_view(), name='create_list_course'),
    path('drafts/', SavedCoursesListView.as_view(), name='list_unpublished_courses'),
    path('<int:pk>/', CourseRetrieveView.as_view(), name='get_course_content'),
    path('enroll/', EnrollInCourse.as_view(), name='enroll'),
    path('mod/', ModulesListCreateView.as_view(), name='create_module'),
    path('mod/<int:pk>/', ModuleRetrieveView.as_view(), name='get_module_content'),
    path('<int:crs_id>/mod/', ModulesListCreateView.as_view(), name='list_modules_in_a_course'),
    path('lsn/', LessonListCreateView.as_view(), name='create_lesson'),
    path('lsn/<int:pk>/', LessonRetrieveView.as_view(), name='get_lesson_content'),
    path('<int:mod_id>/lsn/', LessonListCreateView.as_view(), name='list_lessons_in_a_module'),
    path('ex/', AssignmentListCreateView.as_view(), name='create_assignment'),
    path('ex/<int:pk>/', AssignmentRetrieveView.as_view(), name='get_assignment_content'),
    path('<int:crs_id>/ex/', AssignmentListCreateView.as_view(), name='list_assignments_crs'),
    path('mod/<int:mod_id>/ex/', AssignmentListCreateView.as_view(), name='list_assignments_mod'),
    path('lsn/<int:lsn_id>/ex/',
         AssignmentListCreateView.as_view(),
         name='list_assignments_lsn'),
]
