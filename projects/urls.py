from django.urls import path
from .views import ProjectCreateView

app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name="create"),
]
