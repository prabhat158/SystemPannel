from django.db import models


class ConcertsGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ConcertsEvent(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(ConcertsGenre,
                              related_name='events',
                              on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
