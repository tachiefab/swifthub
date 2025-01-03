from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile
from notifications.models import Notifiction 
from teams.models import Team


# class DashboardView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "accounts/dashboard.html")

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()
        latest_tasks = Task.objects.all()
        latest_members = Profile.objects.all()

        
        context = {}
        if request.user.is_authenticated:
            latest_notifications = Notifiction.objects.for_user(request.user)
            context["latest_notifications"] = latest_notifications[:3]
            context["notification_count"] = latest_notifications.count()
        context["latest_projects"] = latest_projects[:5]
        context["latest_project_count"] = latest_projects.count()
        context["latest_tasks"] = latest_tasks[:5]
        context["latest_task_count"] = latest_tasks.count()
        context["latest_members"] = latest_members[:8]
        context["latest_member_count"] = latest_members.count()
        context["team_count"] = Team.objects.count()
        return render(request, "accounts/dashboard.html", context)
