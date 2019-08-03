from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.


class Fpldata(models.Model):
    data = models.TextField(blank=True, null=True, default='{}')
    import_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["import_date"]
        verbose_name = "FPL Data"
        verbose_name_plural = "FPL Data"

    def __str__(self):
        return self.import_date
