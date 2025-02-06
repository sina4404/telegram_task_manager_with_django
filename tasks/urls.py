from django.urls import path
from .views import TaskListCreateView, TaskUpdateDeleteView

urlpatterns = [
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # Handles GET and POST
    path('api/tasks/<int:pk>/', TaskUpdateDeleteView.as_view(), name='task-update-delete'),  # Handles PATCH and DELETE
]
