from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    pass


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.department}"


class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    job = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.job}"


class HiredEmployee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    datetime = models.DateTimeField(null=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.name}"
