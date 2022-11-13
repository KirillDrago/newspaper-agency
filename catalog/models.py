from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(default="Some content2")
    published_date = models.DateTimeField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers"
    )
