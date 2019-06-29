from django.urls import path
from adplatform.views import CategoryListCreateView

app_name = 'adplatform'

urlpatterns = [
    path('cat/', CategoryListCreateView.as_view(), name='list_create_category'),
]
