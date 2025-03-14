from django.db import models


class ROLES(models.TextChoices):
    ADMIN = 'admin', 'Administrator'
    MANAGER = 'manager', 'Project manager'
    EMPLOYEE = 'employee', 'Employee'
