from django.conf import settings
from django.db import models

from team_finder.constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_MAX_LENGTH,
)


class Project(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    ]

    name = models.CharField("название проекта", max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField("описание проекта", blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="автор проекта",
    )
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    github_url = models.URLField("ссылка на Github", blank=True)
    status = models.CharField(
        "статус",
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        verbose_name="участники",
        blank=True,
    )

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.name
