from django.db import models


class CompetitionsGenre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class CompetitionsEvent(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(CompetitionsGenre,
                              related_name='events',
                              on_delete=models.CASCADE)
    LYP_description = models.TextField(blank=True)
    LYP_img = models.CharField(max_length=30, blank=True)
    LYP_logo = models.ImageField(upload_to='photos/', blank=True)
    LYP_partner = models.CharField(max_length=100, blank=True)
    status = models.TextField(max_length=10, blank=True)
    description = models.TextField()
    queries = models.TextField(blank=True)
    winners = models.TextField(blank=True)
    rules = models.TextField()
    prizes = models.TextField()
    minparticipants = models.IntegerField(default=0)
    maxparticipants = models.IntegerField(default=0)
    subtitle = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MuticityCompetitionsEvent(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name