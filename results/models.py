from django.db import models

# Create your models here.
class ResultsEvent(models.Model):

    DAY = [1,2,3,4]

    DAY_CHOICES = [(c,c) for c in DAY]

    CATEGORY = ['Eliminations',
                'Semi-Finals',
                'Finals',]

    CATEGORY_CHOICES = [(c,c) for c in CATEGORY]

    name = models.CharField(max_length=100,
                            blank=False)

    roundwinners = models.TextField()

    typeofround = models.CharField(max_length=20,
                                   choices = CATEGORY_CHOICES)

    day = models.IntegerField(choices = DAY_CHOICES)


    def __str__(self):
        return self.name
