from django.db import models

class InformalsGenre(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()

    def __str__(self):
        return self.name

class InformalsEvent(models.Model):
    name = models.CharField(max_length = 100)
    genre = models.ForeignKey(InformalsGenre, related_name='events', on_delete = models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name