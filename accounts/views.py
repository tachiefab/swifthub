from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile
from notifications.models import Notifiction 


# class DashboardView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "accounts/dashboard.html")

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()[:5]
        latest_tasks = Task.objects.all()[:5]
        latest_members = Profile.objects.all()[:8]
        latest_notifications = Notifiction.objects.for_user(request.user)
        context = {}
        context["latest_projects"] = latest_projects
        context["latest_tasks"] = latest_tasks
        context["latest_members"] = latest_members
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        return render(request, "accounts/dashboard.html", context)
