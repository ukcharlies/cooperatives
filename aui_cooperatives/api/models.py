from django.contrib.auth.models import User
from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        Faculty, related_name="departments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    employment_number = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"
