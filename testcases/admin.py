from django.contrib import admin

from testcases.models import TestCase, TestCaseType


class TestCaseAdmin(admin.ModelAdmin):
    pass


class TestCaseTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestCaseType, TestCaseTypeAdmin)
