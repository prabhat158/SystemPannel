from django.db import models
from users.models import UserProfile


# Create your models here.
class ContingentLeader(models.Model):

    # Name

    clprofile = models.ForeignKey(UserProfile,
                                  on_delete=models.CASCADE)
    por = models.CharField(max_length=100,
                           blank=False)
    wascllastyear = models.CharField(max_length=3,
                                     blank=False)
    iscrcurrently = models.CharField(max_length=3,
                                     blank=False)
    timesmiattended = models.IntegerField(blank=False)
    nocpiclink = models.TextField()

    def __str__(self):
        return self.clprofile.name

    def get_mi_number(self):
        return self.clprofile.mi_number
    get_mi_number.short_description = u"MI Number"
    get_mi_number.admin_order_field = 'clprofile__mi_number'

    def get_college(self):
        return self.clprofile.present_college.college_name
    get_college.short_description = u"College"
    get_college.admin_order_field = 'clprofile__present_college__college_name'
