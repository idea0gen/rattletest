from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView

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


class TestCaseCreateView(LoginRequiredMixin, CreateView):
    model = TestCase
    fields = [
        "title",
        "description",
        "status",
        "severity",
        "priority",
        "project",
        "testcase_type",
        "pre_condition",
        "post_condition",
    ]
    template_name = "testcase_form.html"

    def form_valid(self, form):
        testcase = form.save(commit=False)
        testcase.created_by = self.request.user
        testcase.save()
        messages.success(self.request, "Testcase added successfully")
        return redirect("about")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TestCaseUpdateView(LoginRequiredMixin, UpdateView):
    model = TestCase
    fields = [
        "title",
        "description",
        "status",
        "severity",
        "priority",
        "project",
        "testcase_type",
        "pre_condition",
        "post_condition",
    ]
    template_name = "testcase_form.html"
    success_message = "Test Case was updated successfully"
    success_url = "/testcase"
