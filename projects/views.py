from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from projects.models import Module, Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["name", "project_code", "description", "members", "owner"]
    template_name = "project_form.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()
        form.save_m2m()
        project.members.add(self.request.user.id)
        messages.success(self.request, "Project added successfully")
        return redirect("projects")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ["name", "project_code", "description", "members", "owner"]
    template_name = "project_update_form.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.modified_by = self.request.user
        project.save()
        form.save_m2m()
        project.members.add(self.request.user.id)
        messages.success(self.request, "Project updated successfully")
        return redirect("projects")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_message(self, cleaned_data):
        name = cleaned_data["name"]
        return self.success_message % dict(
            {
                "cleaned_data": cleaned_data,
                "name": name,
                "object_id": self.kwargs["project_id"],
            }
        )

    def get_success_url(self):
        return redirect("projects")

    def test_func(self):
        if self.request.user == self.get_object().owner:
            return True
        return False
        # members = self.get_object().members.all()
        # if members.contains(self.request.user):
        #     return True
        # return False


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project_list.html"

    def get_queryset(self):
        return (
            Project.objects.filter(members__id__exact=self.request.user.id)
            .order_by("-owner")
            .select_related("owner")
        )


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project

    def get_object(self, queryset=None):
        project = Project.objects.get(id=self.kwargs.get("pk"))
        return project

    def post(self, *args, **kwargs):
        self.get_object().delete()
        payload = {"status": "success", "message": "Project deleted successfully"}

        return JsonResponse(payload)
        # return redirect("projects")

    def test_func(self):
        project = self.get_object()
        if project.owner == self.request.user:
            return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        payload = {
            "status": "fail",
            "message": "You do not have permission, please ask the owner of project to delete",
        }
        # return redirect("project")
        return JsonResponse(payload)


class ModuleCreate(LoginRequiredMixin, CreateView):
    model = Module
    fields = [
        "name",
    ]
    template_name = "module_form.html"

    def form_valid(self, form):
        module = form.save(commit=False)
        module.created_by = self.request.user
        module.modified_by = self.request.user
        module.project = Project.objects.get(id=self.kwargs["project_id"])
        module.save()
        messages.success(self.request, "Module Created successfully")
        return redirect("modules", module.project.id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_message(self, cleaned_data):
        name = cleaned_data["name"]
        return self.success_message % dict(
            {
                "cleaned_data": cleaned_data,
                "name": name,
                "object_id": self.kwargs["project_id"],
            }
        )

    def get_success_url(self):
        return redirect("modules")


class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    fields = [
        "name",
    ]
    template_name = "module_update_form.html"

    def form_valid(self, form):
        module = form.save(commit=False)
        module.modified_by = self.request.user
        module.save()
        messages.success(self.request, "Module updated successfully")
        return redirect("modules", module.project.id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_message(self, cleaned_data):
        name = cleaned_data["name"]
        return self.success_message % dict(
            {
                "cleaned_data": cleaned_data,
                "name": name,
                "object_id": self.kwargs["module_id"],
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        project_id = self.kwargs.get("project_id")
        module_id = self.kwargs.get("module_id")
        queryset = queryset.filter(project=project_id, id=module_id)
        obj = queryset.get()
        return obj


class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "module_list.html"

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs["project_id"])
        return Module.objects.filter(project=project).order_by("-created_date")

    def get_context_data(self, **kwargs):
        context = super(ModuleListView, self).get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs["project_id"])
        return context
