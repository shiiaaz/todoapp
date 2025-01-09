from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Task  # Import the Task model
from .forms import TaskForm  # Assume you have a form class for the Task model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.utils.dateparse import parse_datetime

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                return redirect('login')
            else:
                messages.error(request, 'Username already exists')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'register.html')

# Forgot Password view
def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password successfully changed')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'password_reset.html')

# Dashboard view
def dashboard(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)  # Get tasks for the logged-in user
        return render(request, 'dashboard.html', {'tasks': tasks})
    else:
        return redirect('login')  # Redirect to login if not authenticated

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')  # Optional field

        # Check if due_date is provided and parse it, otherwise set to None
        if due_date:
            due_date = parse_datetime(due_date)
        else:
            due_date = None

        if title and description:
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                user=request.user
            )
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill out all required fields.')
    return render(request, 'dashboard.html')

# Update Task view (mark as completed)
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Get task for the current user
        task.completed = not task.completed  # Toggle completion status
        task.save()
        return redirect('dashboard')  # Redirect to dashboard to view updated task
    except Task.DoesNotExist:
        messages.error(request, 'Task not found or you do not have permission')
        return redirect('dashboard')

# Delete Task view
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Ensure the task belongs to the current user
        task.delete()  # Delete the task
        return redirect('dashboard')  # Redirect to dashboard after deleting the task
    except Task.DoesNotExist:
        messages.error(request, 'Task not found or you do not have permission')
        return redirect('dashboard')

# Task Create View
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Link the task to the logged-in user
        return super().form_valid(form)

# Task Reorder View
class TaskReorder(LoginRequiredMixin, View):
    def post(self, request):
        position_list = request.POST.get('position').split(',')
        with transaction.atomic():
            for i, task_id in enumerate(position_list):
                task = Task.objects.get(id=task_id)
                task.position = i
                task.save()
        return redirect(reverse_lazy('tasks'))

# Task List View
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user).order_by('position')  # Order by position
        return context

# Task Update View
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed']
    success_url = reverse_lazy('tasks')

# Task Delete View
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

from django.db.models import Q

# Task List view with Search and Filter
def task_list(request):
    search_query = request.GET.get('search', '')
    filter_value = request.GET.get('filter', 'all')

    # Always filter by the logged-in user
    tasks = Task.objects.filter(user=request.user)

    if filter_value == 'pending':
        tasks = tasks.filter(completed=False)
    elif filter_value == 'completed':
        tasks = tasks.filter(completed=True)

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    return render(request, 'dashboard.html', {'tasks': tasks})


# Edit Task view
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after editing
    else:
        form = TaskForm(instance=task)

    return render(request, 'update_task.html', {'form': form})
