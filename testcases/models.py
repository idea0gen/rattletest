from django.db import models
from django.urls import reverse

from projects.models import Project
from rattletest.users.models import User

STATUS_CHOICES = ((99, "Not Set"), (10, "Draft"), (20, "In Review"), (30, "Final"))

SEVERITY_CHOICES = (
    (99, "Not Set"),
    (10, "Trivial"),
    (20, "Minor"),
    (30, "Normal"),
    (40, "Major"),
    (50, "Critical"),
)

PRIORITY_CHOICES = ((99, "Not Set"), (10, "Low"), (20, "Medium"), (30, "High"))


class TestCaseType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class TestCase(models.Model):
    created_by = models.ForeignKey(
        User, related_name="testcase", on_delete=models.RESTRICT
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES, blank=True, null=True, default=99
    )
    severity = models.IntegerField(
        choices=SEVERITY_CHOICES, blank=True, null=True, default=99
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, blank=True, null=True, default=99
    )
    testcase_type = models.ForeignKey(
        TestCaseType, on_delete=models.RESTRICT, blank=True, null=True
    )
    pre_condition = models.TextField(blank=True, null=True)
    post_condition = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # attachment = models.FileField(upload_to="uploads/% Y/% m/% d/", max_length=255)

    class Meta:
        ordering = ["-updated_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self, kwargs):
        return reverse("project_detail", kwargs={"pk": self.pk})
