from django.db import models


class Client(models.Model):
    class Type(models.TextChoices):
        LEGAL = 'legal', 'Legal'
        INDIVIDUAL = 'individual', 'Individual'
    name = models.CharField(max_length=150)
    document = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    type = models.CharField(max_length=150, choices=Type, default=Type.LEGAL)

    def __str__(self):
        return self.name
