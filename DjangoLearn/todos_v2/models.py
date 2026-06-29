from django.db import models


class TodoQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(completed=True)

    def pending(self):
        return self.filter(completed=False)


class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TodoQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
