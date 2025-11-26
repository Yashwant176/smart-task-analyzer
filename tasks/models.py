from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=300)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(default=1.0)
    importance = models.IntegerField(default=5)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependents')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"
