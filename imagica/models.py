from django.db import models

class rider(models.Model):
    name = models.CharField(max_length=300)
    mobile_number = models.CharField(max_length=11)
    email = models.CharField(max_length=300)
    ticketPrice = models.IntegerField(blank=False)
    ticketName = models.CharField(max_length=500)
    college = models.CharField(max_length=500)
    cr_referral_code = models.CharField(max_length=8, blank=True, null=True)
    bus_pickup = models.CharField(max_length=35, blank=True)

# Create your models here.
