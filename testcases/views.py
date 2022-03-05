from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView

from projects.models import Project
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
        return TestCase.objects.filter(project=project)

    def get_context_data(self, **kwargs):
        context = super(TestCaseListView, self).get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs["project_id"])
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
    ]
    template_name = "testcase_form.html"

    def form_valid(self, form):
        testcase = form.save(commit=False)
        testcase.project = Project.objects.get(id=self.kwargs["project_id"])
        testcase.created_by = self.request.user
        testcase.modified_by = self.request.user
        testcase.save()
        messages.success(self.request, "Testcase added successfully")
        return redirect("testcases", testcase.project.id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        print("test_func")
        print(self.kwargs["project_id"])
        return True


class TestCaseUpdateView(LoginRequiredMixin, UpdateView):
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
    ]

    def form_valid(self, form):
        testcase = form.save(commit=False)
        testcase.modified_by = self.request.user
        testcase.project = Project.objects.get(id=self.kwargs["project_id"])
        testcase.save()
        messages.success(self.request, "Testcase updated successfully")
        return redirect("testcases", testcase.project.id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    template_name = "testcase_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(id=self.kwargs["project_id"])
        return context
