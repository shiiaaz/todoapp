from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from base import views

urlpatterns = [
     # User Authentication
    path("register/", views.register_view, name="register"),  
    path("login/", views.login_view, name="login"),           

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"), 

    # Task Management
    path('', lambda request: redirect('login')),  
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('', views.TaskList.as_view(), name='tasks'),
    path('task/create/', views.TaskCreate.as_view(), name='task-create'),
    path('task/reorder/', views.TaskReorder.as_view(), name='task-reorder'),
    path('task/update/<int:task_id>/', views.update_task, name='update_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/', views.task_list, name='task-list'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/<int:pk>/update/', views.TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDelete.as_view(), name='task-delete'),
]
