from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Allow empty descriptions
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "user"
