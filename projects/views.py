from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
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
        if self.request.user.is_authenticated:
            latest_notifications = self.request.user.notifications.unread()
            
            context = super(ProjectCreateView, self).get_context_data(**kwargs)
            context["latest_notifications"] = latest_notifications[:3]
            context["notification_count"] = latest_notifications.count()
            context["header_text"] = "Project Add"
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



