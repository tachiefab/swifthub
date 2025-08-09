from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from teams.models import Team
from .utils import STATUS_CHOICES, PRIORITY_CHOICES



class ProjectQueryset(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcoming(self):
        return self.filter(due_date__gte=timezone.now())
    
    def due_in_two_days_or_less(self):
        today = timezone.now().date()
        two_days_from_today = today + timedelta(days=2)
        return self.active().upcoming().filter(due_date__lte=two_days_from_today)
    
    # user and team owned projects
    def for_user(self, user):
        return self.filter(models.Q(owner=user) | models.Q(team__members=user)).distinct()
    

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQueryset(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active().upcoming()
    
    def due_in_two_days_or_less(self):
         return self.get_queryset().active().upcoming().due_in_two_days_or_less()
    
    def for_user(self, user):
        return self.get_queryset().active().upcoming().for_user(user)


    

    
    
  

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    client_company = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To Do")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")

    # budget details
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    estimated_duration = models.IntegerField(blank=True, null=True, help_text="Estimated duration in days")
    start_date = models.DateField()
    due_date = models.DateField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

    
    def days_until_due(self):
        if self.due_date:
            #get current date
            current_date = timezone.now().date()
            return (self.due_date - current_date).days
        return None
    
    @property
    def progress(self):
        progress_dict ={
            'To Do': 0,
            'In Progress': 50,
            'Completed': 100,
        }
        return progress_dict.get(self.status, 0)
    

    @property
    def status_color(self):
        status_value = self.progress
        if status_value == 100:
            color = "success"
        elif status_value == 50:
            color = "primary"
        else:
            color = ""
        return color

           
    

    def priority_color(self):
        if self.priority == "Low":
            color = "success"
        elif self.priority == "Medium":
            color = "warning"
        else:
            color = "danger"
        return color
    

#project file location
def project_attachment_path_location(instance, filename):
    # get todays date YYYY-MM-DD format
    today_date = datetime.now().strftime('%Y-%m-%d')
    #return the upload path
    return "attachments/%s/%s/%s" % (instance.project.name, today_date, filename)
   

class Attachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='attachments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=project_attachment_path_location)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment by {self.user.username} on {self.project.name}"
    

