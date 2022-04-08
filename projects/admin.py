from django.contrib import admin

from .models import Module, Project


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"project_slug": ("name",)}


class ModuleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)

admin.site.register(Module, ModuleAdmin)
