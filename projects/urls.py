from django.urls import path
from .views import ProjectCreateView, ProjectListView, ProjectNearDueDateListView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name="list"),
    path('create/', ProjectCreateView.as_view(), name="create"),
    path('near-due-date', ProjectNearDueDateListView.as_view(), name="due-list"),
]
