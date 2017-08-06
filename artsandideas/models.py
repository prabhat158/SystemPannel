from django.db import models


class ArtsAndIdeasGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ArtsAndIdeasEvent(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(ArtsAndIdeasGenre,
                              related_name='genres',
                              on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
