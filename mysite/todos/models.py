from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    # id
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

