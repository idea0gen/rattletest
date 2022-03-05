from django.urls import path

from testcases import views

urlpatterns = [
    path(
        "project/<int:project_id>/testcase/create/",
        views.TestCaseCreateView.as_view(),
        name="new_testcase",
    ),
    path(
        "project/<int:project_id>/testcase/<int:testcase_id>/edit",
        views.TestCaseUpdateView.as_view(),
        name="edit_testcase",
    ),
    path(
        "project/<int:project_id>/testcase/",
        views.TestCaseListView.as_view(),
        name="testcases",
    ),
]
