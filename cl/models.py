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

'''
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
'''

class ContingentMember(models.Model):

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_selected = models.IntegerField(blank=False, default=0)
    is_imp = models.IntegerField(blank=False, default=0)
    has_paid = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.profile.name

    def get_name(self):
        return self.profile.name
    get_name.short_description = u"Name"
    get_name.admin_order_field = 'profile__name'

    def get_mi_number(self):
        return self.profile.mi_number
    get_mi_number.short_description = u"MI Number"
    get_mi_number.admin_order_field = 'profile__mi_number'

    def get_email(self):
        return self.profile.email
    get_email.short_description = u"Email"
    get_email.admin_order_field = 'profile__email'

    def get_mobile_number(self):
        return self.profile.mobile_number
    get_mobile_number.short_description = u"Phone"
    get_mobile_number.admin_order_field = 'profile__mobile_number'



class Contingent(models.Model):

    cl = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)
    contingent_members = models.ManyToManyField(ContingentMember, blank=True)
    contingent_strength = models.IntegerField(blank=False, default=0)
    selected_contingent_strength = models.IntegerField(blank=False, default=0)
    is_equal = models.IntegerField(blank=False, default=0)
    strength_alloted = models.IntegerField(blank=False, default=-1)
    is_approved = models.IntegerField(blank=False, default=0)
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.cl.name

    def get_cl_name(self):
        return self.cl.name
    get_cl_name.short_description = u"Name"
    get_cl_name.admin_order_field = 'cl__name'


    def get_cl_mi_number(self):
        return self.cl.mi_number
    get_cl_mi_number.short_description = u"UserName"
    get_cl_mi_number.admin_order_field = 'cl__mi_number'


    def get_cl_pass(self):
        return self.cl.fb_id
    get_cl_pass.short_description = u"Password"
    get_cl_pass.admin_order_field = 'cl__fb_id'

    def get_cl_college(self):
        return self.cl.present_college.college_name
    get_cl_college.short_description = u"College"
    get_cl_college.admin_order_field = 'cl__present_college__college_name'

    def get_cl_city(self):
        return self.cl.present_city.city_name
    get_cl_city.short_description = u"City"
    get_cl_city.admin_order_field = 'cl__present_city__city_name'

    def get_members(self):
        return "\n".join([p.profile.name+' '+str(p.is_selected)+' '+str(p.has_paid)+' '+str(p.is_imp) for p in self.contingent_members.all()])  
