from django.db import models


class News(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField()
