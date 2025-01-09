from django import forms
from .models import Task  # Import the Task model

# Reordering Form
class PositionForm(forms.Form):
    position = forms.CharField()

# Task Form
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']  # Add
