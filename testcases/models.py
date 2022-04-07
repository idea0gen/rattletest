import os

from django.contrib.auth import get_user_model
from django.db import models

from projects.models import Module, Project
from rattletest.users.models import User

STATUS_CHOICES = ((10, "Draft"), (20, "In Review"), (30, "Final"))

SEVERITY_CHOICES = (
    (10, "Trivial"),
    (20, "Minor"),
    (30, "Normal"),
    (40, "Major"),
    (50, "Critical"),
)

PRIORITY_CHOICES = ((10, "Low"), (20, "Medium"), (30, "High"))


class TestCaseType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


def get_deleted_user_instance():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class TestCase(models.Model):

    created_by = models.ForeignKey(
        User,
        related_name="tc_created_by",
        on_delete=models.SET(get_deleted_user_instance),
    )
    modified_by = models.ForeignKey(
        User,
        related_name="tc_modified_by",
        on_delete=models.SET(get_deleted_user_instance),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES, blank=True, null=True, default=10
    )
    severity = models.IntegerField(
        choices=SEVERITY_CHOICES, blank=True, null=True, default=30
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, blank=True, null=True, default=20
    )
    testcase_type = models.ForeignKey(
        TestCaseType, on_delete=models.RESTRICT, blank=True, null=True
    )
    pre_condition = models.TextField(blank=True, null=True)
    post_condition = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    attachment = models.FileField(
        upload_to="uploads/%Y/%m/%d/", max_length=255, blank=True, null=True
    )

    class Meta:
        ordering = ["-updated_date"]

    def __str__(self):
        return self.title

    def filename(self):
        print("self.attachment.name", self.attachment.name)
        return os.path.basename(self.attachment.name)
