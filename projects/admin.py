from django.contrib import admin
from . models import Project, Attachment
from notifications.tasks import create_notification


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'owner',
        'team',
        'status',
        'priority',
        'start_date',
        'due_date'
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner=request.user
            verb = f'New Project Assignment, {obj.name}'
        else:
            verb = f'Project Updated, {obj.name}'
        
        super().save_model(request, obj, form, change) #saving our project

         # send notification
        actor_username = request.user.username
        object_id = obj.id

        create_notification.delay(
                actor_username=actor_username,  
                verb=verb, 
                object_id=object_id
                )   

admin.site.register(Project, ProjectAdmin)

admin.site.register(Attachment)