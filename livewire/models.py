from django.db import models


# Create your models here.
class LivewireBand(models.Model):
    CITY = ['pune',
            'bangalore',
            'delhi',
            'shillong',
            'mumbai', ]

    CITY_CHOICES = [(c, c) for c in CITY]

    # Name

    band_name = models.CharField(max_length=100,
                                 blank=False)
    facebook_link = models.CharField(max_length=200,
                                     blank=False)
    manager = models.CharField(max_length=100,
                               blank=False)
    emailid = models.CharField(max_length=200,
                               unique=True,
                               blank=False)
    mobile_number = models.CharField(max_length=10,
                                     unique=True,
                                     blank=False)
    bandmembers = models.TextField()
    hometown = models.CharField(max_length=100,
                                blank=False)
    preferred_city = models.CharField(max_length=10,
                                      choices=CITY_CHOICES)
    original_composition = models.CharField(max_length=200,
                                            blank=False)

    def __str__(self):
        return self.band_name
