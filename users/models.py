from django.db import models
from competitions.models import CompetitionsEvent


class City(models.Model):
    city_name = models.CharField(max_length=20)

    def __str__(self):
        return self.city_name


class College(models.Model):
    college_name = models.CharField(max_length=50)
    located_city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.college_name


class UserProfile(models.Model):
    YEAR = ['First',
            'Second',
            'Third',
            'Fourth',
            'Fifth', ]

    YEAR_CHOICES = [(c, c) for c in YEAR]

    # Name

    name = models.CharField(max_length=50,
                            blank=False)

    # Non-blank and Unique fields

    mi_number = models.CharField(max_length=11,
                                 unique=True,
                                 blank=False)

    fb_id = models.IntegerField(unique=True,
                                blank=False)

    email = models.EmailField(max_length=70,
                              unique=True,
                              blank=False)

    mobile_number = models.IntegerField(unique=True,
                                        blank=False)

    # City and College

    present_city = models.ForeignKey(City,
                                     on_delete=models.CASCADE,
                                     null=True)

    present_college = models.ForeignKey(College,
                                        on_delete=models.CASCADE,
                                        null=True)

    # Address

    postal_address = models.CharField(max_length=100, blank=False)

    zip_code = models.IntegerField(blank=False)

    # Year of study

    year_of_study = models.CharField(max_length=7, choices=YEAR_CHOICES)

    def __str__(self):
        return self.name

    def set_mi_number(self, no):
        self.mi_number = no

    def getName(self):
        return self.name


class Group(models.Model):

    name = models.CharField(max_length=11)
    event = models.ForeignKey(CompetitionsEvent,
                              on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile,
                                     blank=True)

    def __str__(self):
        return self.name
