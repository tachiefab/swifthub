from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from projects.models import Project
from tasks.models import Task
from .models import Profile
# from notifications.models import Notifiction 
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
        # if request.user.is_authenticated:
        latest_notifications = request.user.notifications.unread()
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["latest_projects"] = latest_projects[:5]
        context["latest_project_count"] = latest_projects.count()
        context["projects_near_due_date"] = latest_projects.due_in_two_days_or_less()[:5]
        # context["latest_task_count"] = latest_tasks.count()
        context["latest_members"] = latest_members[:8]
        context["latest_member_count"] = latest_members.count()
        context["team_count"] = Team.objects.count()
        context["header_text"] = "Dashboard"
        context["title"] = "Dashboard"
        return render(request, "accounts/dashboard.html", context)


class MembersListView(ListView):
    model = Profile
    context_object_name = "members"
    template_name = "accounts/profile_list.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(MembersListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread()            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Members"
        context["title"] = "All Members"
        return context