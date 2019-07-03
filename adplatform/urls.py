from django.urls import path
from adplatform.views import CategoryListCreateView, TagListCreateView

app_name = 'adplatform'

urlpatterns = [
    path('cat/', CategoryListCreateView.as_view(), name='list_create_category'),
    path('tag/', TagListCreateView.as_view(), name='list_create_tag')
]
