from django.shortcuts import redirect
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import CreateView, ListView, DetailView
from .models import Project
from .forms import ProjectForm, AttachmentForm
from comments.models import Comment
from comments.forms import CommentForm
from tasks.forms import TaskUpdateForm

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
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
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

        create_notification.delay(
                actor_username=actor_username,  
                verb=verb, 
                object_id=project.id
                )      
        return redirect(self.success_url)

    
class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/project_list.html"
    paginate_by = 2

    def get_queryset(self):
        return Project.objects.for_user(self.request.user)
    

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
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
        return Project.objects.for_user(self.request.user).due_in_two_days_or_less()

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectNearDueDateListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Due Projects"
        return context
    

class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user) 
        project = self.get_object()            
        comments =   Comment.objects.filter_by_instance(project)  
        paginator = Paginator(comments, 5) 
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Project Detail"
        context["title"] = project.name
        context["my_company"] = "Swifthub"
        context["my_company_description"] = """
            Swifthub is a robust Project Management System that streamlines task tracking, 
            team collaboration, and progress monitoring, ensuring projects stay on track and 
            deadlines are met efficiently.
        """
        context["page_obj"] = page_obj
        context["comments_count"] = comments.count()
        context["comment_form"] = CommentForm()
        context["attachment_form"] = AttachmentForm()
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user not in project.team.members.all():
            messages.warning(request, "You are not a member of this project and you cannot comment")
            return self.get(request, *args, **kwargs)

        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.content_object = project
                comment.save()

                # send notification
                actor_username = self.request.user.username
                actor_full_name = self.request.user.profile.full_name
                verb = f'{actor_full_name}, commented on {project.name}'

                create_notification.delay(
                        actor_username=actor_username,  
                        verb=verb, 
                        object_id=project.id
                        )   
                messages.success(request, "Your comment has been added successfully")
                return redirect('projects:project-detail', pk=project.pk)
            else:
                messages.warning(request, form.errors.get("comment", ["An unknown error occured."])[0])
        
        if 'attachment_submit' in request.POST:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.project = project
                attachment.user = request.user
                attachment.save()
                messages.success(request, "Your file has been uploaded successfully")
                return redirect('projects:project-detail', pk=project.pk)
            else:
                messages.error(request, "Error uploading the file, please try again later")
                
        return self.get(request, *args, **kwargs)
            
            

class KanbanBoardView(DetailView):
    model = Project
    template_name = "projects/kanbanboard.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(KanbanBoardView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user) 
        project = self.get_object()         
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Kanban Board"
        context["title"] = f"{project.name}'s Kanban Board"
        context["is_kanban"] = True

        # separate tasks by status
        context["backlog_tasks"] = project.tasks.filter(status="Backlog").upcoming()
        context["todo_tasks"] = project.tasks.filter(status="To Do").upcoming()
        context["in_progress_tasks"] = project.tasks.filter(status="In Progress").upcoming()
        context["completed_tasks"] = project.tasks.filter(status="Completed").upcoming()
        context['form'] = TaskUpdateForm()
        
        return context


