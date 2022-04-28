from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView

from projects.models import Module, Project
from testcases.models import TestCase


class TestCaseListView(LoginRequiredMixin, ListView):
    model = TestCase
    fields = [
        "title",
        "status",
        "priority",
        "testcase_type",
        "created_date",
        "updated_date",
        "created_by",
    ]
    template_name = "testcase_list.html"

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs["project_id"])
        module = get_object_or_404(Module, id=self.kwargs["module_id"])
        return TestCase.objects.filter(project=project, module=module)

    def get_context_data(self, **kwargs):
        context = super(TestCaseListView, self).get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs["project_id"])
        context["module"] = Module.objects.get(id=self.kwargs["module_id"])
        print("context is:", context)
        return context


class TestCaseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TestCase
    fields = [
        "title",
        "description",
        "status",
        "severity",
        "priority",
        "testcase_type",
        "pre_condition",
        "post_condition",
        "attachment",
        "project",
        "module",
    ]
    template_name = "testcase_form.html"

    def form_valid(self, form):
        testcase = form.save(commit=False)
        testcase.created_by = self.request.user
        testcase.modified_by = self.request.user
        testcase.attachment = self.request.FILES.get("attachment")
        testcase.save()
        messages.success(self.request, "Testcase added successfully")
        return redirect("testcases", testcase.project.id, testcase.module.id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        project = Project.objects.get(id=self.kwargs["project_id"])
        user_projects = self.request.user.projects.all()
        if project in user_projects:
            return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        messages.error(
            self.request,
            "You do not have permission, please ask the owner of project to provide you permission",
        )
        return redirect("projects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        # context["module"] = Module.objects.filter(id=self.kwargs["module_id"])
        context["modules"] = Module.objects.all()
        context["project"] = Project.objects.get(id=self.kwargs["project_id"])
        context["module"] = Module.objects.get(id=self.kwargs["module_id"])
        return context


class TestCaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TestCase
    fields = [
        "title",
        "description",
        "status",
        "severity",
        "priority",
        "testcase_type",
        "pre_condition",
        "post_condition",
        "attachment",
        "project",
        "module",
    ]

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        project_id = self.kwargs.get("project_id")
        module_id = self.kwargs.get("module_id")
        testcase_id = self.kwargs.get("testcase_id")
        try:
            obj = get_object_or_404(
                TestCase, project=project_id, module=module_id, id=testcase_id
            )
            return obj
        except Exception as e:
            print("Exception is:", e)

    def get(self, *args, **kwargs):
        if self.model.objects.filter(
            id=self.kwargs["testcase_id"],
            project=self.kwargs["project_id"],
            module=self.kwargs["module_id"],
        ).exists():
            return super().get(*args, **kwargs)
        else:
            messages.error(
                self.request, "Testcase not found, please create a new test case"
            )
            return redirect(
                "testcases", self.kwargs["project_id"], self.kwargs["module_id"]
            )

    def test_func(self):
        project = Project.objects.get(id=self.kwargs["project_id"])
        user_projects = self.request.user.members.all()
        if project in user_projects:
            return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        messages.error(
            self.request,
            "You do not have permission, please ask the owner of project to provide you permission",
        )
        return redirect("projects")

    def form_valid(self, form):
        testcase = form.save(commit=False)
        testcase.modified_by = self.request.user
        testcase.save()
        messages.success(self.request, "Testcase updated successfully")
        return redirect("testcases", testcase.project.id, testcase.module_id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    template_name = "testcase_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        context["modules"] = Module.objects.all()
        return context
