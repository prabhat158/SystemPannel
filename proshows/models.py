from django.db import models


class ProshowsGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProshowsEvent(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(ProshowsGenre,
                              related_name="events",
                              on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
