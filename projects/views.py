from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView

from projects.models import Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["name", "project_code", "description"]
    template_name = "project_form.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()
        messages.success(self.request, "Project added successfully")
        return redirect("projects")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ["name", "project_code", "description"]
    template_name = "project_update_form.html"

    success_message = "%(name)s was updated successfully"
    # success_url = reverse_lazy('my_receipe') # no qa if no param is required, can use as is
    # permission_required = "meals.change_meal"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()
        messages.success(self.request, "Project updated successfully")
        return redirect("projects")

    def form_invalid(self, form):
        print("Form is invalid")
        print("Form Errors are Data is:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_message(self, cleaned_data):
        name = cleaned_data["name"]
        return self.success_message % dict(
            {
                "cleaned_data": cleaned_data,
                "name": name,
                "object_id": self.kwargs["pk"],
            }
        )

    def get_success_url(self):
        return redirect("/")


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project_list.html"
