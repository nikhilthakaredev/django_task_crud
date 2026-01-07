from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, task_list, task_create, task_update, task_delete,task_pie_chart,task_bar_graph

router = DefaultRouter()
router.register('api/tasks', TaskViewSet)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('update/<int:pk>/', task_update, name='task_update'),
    path('delete/<int:pk>/', task_delete, name='task_delete'),
    path('chart/pie/', task_pie_chart, name='task_pie_chart'),
    path('chart/bar/', task_bar_graph, name='task_bar_graph'),
    path('', include(router.urls)),
]
