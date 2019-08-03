from django.urls import path
from adplatform.views import CategoryListCreateView, TagListCreateView, FeedbackListView, FeedbackCreateView

app_name = 'adplatform'

urlpatterns = [
    path('cat/', CategoryListCreateView.as_view(), name='list_create_category'),
    path('tag/', TagListCreateView.as_view(), name='list_create_tag'),
    path('feedback/', FeedbackCreateView.as_view(), name='create_feedback'),
    path('getfeeds/', FeedbackListView.as_view(), name='list_feedback')
]
