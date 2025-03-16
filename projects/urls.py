from django.urls import path
from .views import (
    ProjectCreateView, 
    ProjectListView, 
    ProjectNearDueDateListView,
    ProjectDetailView,
    KanbanBoardView
    )

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name="list"),
    path('create/', ProjectCreateView.as_view(), name="create"),
    path('near-due-date', ProjectNearDueDateListView.as_view(), name="due-list"),
    path('<uuid:pk>', ProjectDetailView.as_view(), name="project-detail"),
    path('<uuid:pk>/kanban-board', KanbanBoardView.as_view(), name="kanban-board"),
]
