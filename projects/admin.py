from django.contrib import admin

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"project_slug": ("name",)}


admin.site.register(Project, ProjectAdmin)
