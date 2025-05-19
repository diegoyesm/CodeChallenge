from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Department, Job, HiredEmployee, CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = (
        "id", "department",
    )
    list_display = (
        "id", "department",
    )
    readonly_fields = ()


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    fields = (
        "id", "job",
    )
    list_display = (
        "id", "job",
    )
    readonly_fields = ()


@admin.register(HiredEmployee)
class HiredEmployeeAdmin(admin.ModelAdmin):
    fields = (
        "id", "name", "datetime", "department_id", "job_id",
    )
    list_display = (
        "id", "name", "datetime", "department_id", "job_id",
    )
    readonly_fields = (
        "datetime",
    )
