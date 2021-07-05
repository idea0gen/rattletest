from django.urls import path

from testcases import views

urlpatterns = [
    path("testcase/create/", views.TestCaseCreateView.as_view(), name="new_testcase"),
    path(
        "testcase/<int:pk>/edit",
        views.TestCaseUpdateView.as_view(),
        name="edit_testcase",
    ),
]
