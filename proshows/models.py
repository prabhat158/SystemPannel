from django.db import models


class ProshowsGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ProshowsEvent(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(ProshowsGenre,
                              related_name="events",
                              on_delete=models.CASCADE)
    description = models.TextField()
    subtitle = models.CharField(max_length=100)
    image = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name
