from django.db import models


class CompetitionsGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CompetitionsEvent(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(CompetitionsGenre,
                              related_name='events',
                              on_delete=models.CASCADE)
    description = models.TextField()
    rules = models.TextField()
    prizes = models.TextField()
    minparticipants = models.IntegerField(default=0)
    maxparticipants = models.IntegerField(default=0)

    def __str__(self):
        return self.name
