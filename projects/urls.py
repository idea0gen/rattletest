from django.urls import path

from projects import views

urlpatterns = [
    path("project/create/", views.ProjectCreate.as_view(), name="new_project"),
    path(
        "project/<int:pk>/edit/",
        views.ProjectUpdateView.as_view(),
        name="project_edit",
    ),
    path("project/", views.ProjectListView.as_view(), name="projects"),
    path(
        "project/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project_delete",
    ),
    path(
        "project/<int:project_id>/module/create/",
        views.ModuleCreate.as_view(),
        name="new_module",
    ),
    path(
        "project/<int:project_id>/module/<int:module_id>/edit/",
        views.ModuleUpdateView.as_view(),
        name="module_edit",
    ),
    path(
        "project/<int:project_id>/module",
        views.ModuleListView.as_view(),
        name="modules",
    ),
]
