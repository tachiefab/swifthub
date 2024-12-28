from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile


# class DashboardView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "accounts/dashboard.html")

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()[:5]
        latest_tasks = Task.objects.all()[:5]
        latest_members = Profile.objects.all()[:8]
        context = {}
        context["latest_projects"] = latest_projects
        context["latest_tasks"] = latest_tasks
        context["latest_members"] = latest_members
        return render(request, "accounts/dashboard.html", context)
