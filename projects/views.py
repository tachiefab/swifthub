from django.shortcuts import redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Project
from .forms import ProjectForm

from notifications.tasks import create_notification

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy("accounts:dashboard")

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread()            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Project Add"
        context["title"] = "Project Add"
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        # send notification
        actor_username = self.request.user.username
        verb = f'New Project Assignment, {project.name}'
        object_id = project.id

        create_notification.delay(
                actor_username=actor_username,  
                verb=verb, 
                object_id=object_id
                )      
        return redirect(self.success_url)

    
class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/project_list.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread()            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Projects"
        context["title"] = "All Projects"
        return context



class ProjectNearDueDateListView(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/project_list.html"
    paginate_by = 2

    def get_queryset(self):
        return Project.objects.all().due_in_two_days_or_less()

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectNearDueDateListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread()            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Due Projects"
        return context
    



