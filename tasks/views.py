from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from .models import Task
from projects.models import Project
from .forms import TaskUpdateForm


@require_POST
def update_task_status_ajax(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)

        new_status = data.get('status').title()
        print(new_status)

        # check if status is valid
        if new_status in ['Backlog', 'To Do', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    

@require_POST
def create_task_ajax(request):
    name = request.POST.get('name')
    project_id = request.POST.get('project_id')
    user = request.user

    if not name:
        return JsonResponse({'success': False, 'error': 'Task title is required'})
    
    if not project_id:
        return JsonResponse({'success': False, 'error': 'Project ID is required'})
    
    try:
        project = Project.objects.get(id=project_id)

        # create new task
        new_task = Task.objects.create(name=name, project=project, owner=user)

        return JsonResponse({'success': True, 'task_id': new_task.id})
    except Project.DoesNotExist:
         return JsonResponse({'success': False, 'error': 'Project not found'})
    


def get_task(request, task_id):
    # get by id
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, stutus=404)
    
    if request.method == "GET":
         # construct a json response
         task_data =  {
             "id": str(task.id),
             "name": task.name,
             "description": task.description,
            "priority": task.priority,
             "start_date": task.start_date.isoformat() if task.start_date else "",
             "due_date": task.due_date.isoformat() if task.due_date else "",
         }

         return JsonResponse({"task_data": task_data})
    

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

            # return response
            return JsonResponse({
            'success': True,
            'updatedTask':  {
             "id": str(task.id),
             "name": task.name,
             "description": task.description,
             "start_date": task.start_date.isoformat() if task.start_date else "",
             "due_date": task.due_date.isoformat() if task.due_date else "",
         }
            })
        else:
            # return form errors
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


    
   
