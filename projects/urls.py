from django.urls import path

from projects import views

urlpatterns = [
    path("project/create/", views.ProjectCreate.as_view(), name="new_project"),
    path(
        "project/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"
    ),
    path("project/", views.ProjectListView.as_view(), name="projects"),
]
