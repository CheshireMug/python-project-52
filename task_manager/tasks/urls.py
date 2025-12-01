from django.urls import path
from .views import TasksListView, TaskCreateView, \
    TaskUpdateView, TaskDeleteView

app_name = 'tasks'

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='tasks_create'),
    path(
        '<int:pk>/update/',
        TaskUpdateView.as_view(),
        name='tasks_update'
        ),
    path(
        '<int:pk>/delete/',
        TaskDeleteView.as_view(),
        name='tasks_delete'
        ),
]
