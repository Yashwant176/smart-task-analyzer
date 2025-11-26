from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'importance', 'estimated_hours', 'due_date')
    search_fields = ('title',)
