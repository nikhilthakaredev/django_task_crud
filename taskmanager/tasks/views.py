from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import Task
import matplotlib
matplotlib.use('Agg')  # non-GUI backend (fixes the error)

import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import Task

# =========================
# REST API CRUD
# =========================
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# =========================
# HTML CRUD (Bootstrap)
# =========================
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            completed=True if request.POST.get('completed') == 'on' else False
        )
        return redirect('task_list')
    return render(request, 'tasks/task_form.html')


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = True if request.POST.get('completed') == 'on' else False
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {'task': task})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})



def task_pie_chart(request):
    completed = Task.objects.filter(completed=True).count()
    pending = Task.objects.filter(completed=False).count()

    labels = ['Completed', 'Pending']
    sizes = [completed, pending]

    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Task Completion Status')
    plt.axis('equal')

    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()

    return response

def task_bar_graph(request):
    completed = Task.objects.filter(completed=True).count()
    pending = Task.objects.filter(completed=False).count()

    categories = ['Completed', 'Pending']
    values = [completed, pending]

    plt.figure()
    plt.bar(categories, values)
    plt.xlabel('Task Status')
    plt.ylabel('Number of Tasks')
    plt.title('Task Report')

    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()

    return response