from django.db import models
from users.models import UserProfile, College, City


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

    class Meta:
        ordering = ['-id']

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

class Contingent(models.Model):

    cl = models.ForeignKey(ContingentLeader, on_delete=models.CASCADE)
    cl_name = models.CharField(max_length=50,
                               blank=False)
    cl_mobile_number = models.CharField(max_length=10,
                                        blank=False)
    contingent_college = models.ForeignKey(College,
                                           on_delete=models.CASCADE,
                                           null=True)
    contigent_city = models.ForeignKey(City,
                                       on_delete=models.CASCADE,
                                       null=True)
    contingent_members = models.ManyToManyField(UserProfile,
                                                blank=True)

    contingent_strength = models.IntegerField(blank=False)
    strength_alloted = models.IntegerField(blank=False)
    status = models.IntegerField(blank=False)

    def __str__(self):
        return self.cl_name