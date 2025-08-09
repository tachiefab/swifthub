from django.urls import path
from .views import (
    ProjectCreateView, 
    ProjectListView, 
    ProjectNearDueDateListView,
    ProjectDetailView,
    KanbanBoardView,
    ProjectDeleteView,
    ProjectUpdateView
    )

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name="list"),
    path('create/', ProjectCreateView.as_view(), name="create"),
    path('near-due-date', ProjectNearDueDateListView.as_view(), name="due-list"),
    path('<uuid:pk>', ProjectDetailView.as_view(), name="project-detail"),
    path('<uuid:pk>/delete/', ProjectDeleteView.as_view(), name="delete"),
    path('<uuid:pk>/update/', ProjectUpdateView.as_view(), name="update"),
    path('<uuid:pk>/kanban-board', KanbanBoardView.as_view(), name="kanban-board"),
]
