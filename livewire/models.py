from django.db import models


# Create your models here.
class LivewireBand(models.Model):
    CITY = ['pune',
            'bangalore',
            'delhi',
            'shillong',
            'mumbai', ]

    CITY_CHOICES = [(c, c) for c in CITY]
    city = models.CharField(max_length=100,
                                 blank=False)
    # Name

    band_name = models.CharField(max_length=100,
                                 blank=False)
    facebook_link = models.TextField()
    emailid = models.CharField(max_length=200,
                               blank=False)
    mobile_number = models.CharField(max_length=100,
                                     blank=False)
    bandmembers = models.TextField()
    preferred_city = models.CharField(max_length=10,
                                      choices=CITY_CHOICES, blank=True)
    original_composition = models.TextField(blank=True)

    def __str__(self):
        return self.band_name
