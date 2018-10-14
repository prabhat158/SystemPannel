from django.db import models
from competitions.models import CompetitionsEvent
from workshops.models import WorkshopsEvent


class ActualCity(models.Model):
    city_name = models.CharField(max_length=100)
    def __str__(self):
        return self.city_name

class ActualCollege(models.Model):
    college_name = models.CharField(max_length=300)
    city = models.ForeignKey(ActualCity, blank=True, null=True, on_delete=models.CASCADE)
    assignedcl = models.ForeignKey('UserProfile', blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.college_name

class City(models.Model):
    city_name = models.CharField(max_length=100)
    actual_city = models.ForeignKey(ActualCity, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name


class College(models.Model):
    college_name = models.CharField(max_length=300)
    located_city = models.ForeignKey(City, on_delete=models.CASCADE)
    actual_college = models.ForeignKey(ActualCollege, blank=True, null=True, on_delete=models.CASCADE)
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

    google_id = models.CharField(max_length=30,
                             unique=True,
                             blank=False)

    email = models.EmailField(max_length=100,
                              unique=True,
                              blank=False)

    cr_referral_code=models.CharField(max_length=7, null=True, blank=True)

    mobile_number = models.CharField(max_length=10,
                                     unique=True,
                                     blank=False)

    # City and College

    present_city = models.ForeignKey(City,
                                     on_delete=models.CASCADE,
                                     null=True)

    present_college = models.ForeignKey(College,
                                        on_delete=models.CASCADE,
                                        null=True)

    # Address

    postal_address = models.CharField(max_length=100,
                                      blank=False)
    permanent_address = models.CharField(max_length=200, blank=False, default='NULL')

    zip_code = models.IntegerField(blank=False)
    gender = models.CharField(blank=False, default='NULL', max_length=7)

    # Year of study and birthdate

    dob = models.CharField(default="0",
                           max_length=10,
                           blank=False)

    year_of_study = models.CharField(max_length=7,
                                     choices=YEAR_CHOICES)

    checkedin = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def set_mi_number(self, no):
        self.mi_number = no

    def getName(self):
        return self.name

    '''def get_cl_name(self):
        cl = self.present_college.assignedcl
        if(cl is None):
            return None
        else:
            return cl.name
    get_cl_name.short_description = u"CL"

    def get_cl_mail(self):
        cl = self.present_college.assignedcl
        if(cl is None):
            return None
        else:
            return cl.email
    get_cl_name.short_description = u"CL mail"
    def get_cl_number(self):
        cl = self.present_college.assignedcl
        if(cl is None):
            return None
        else:
            return cl.mobile_number
    get_cl_name.short_description = u"CL number"'''


class Group(models.Model):

    name = models.CharField(max_length=600)
    event = models.ForeignKey(CompetitionsEvent,
                              on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10,
                                     blank=False)
    present_city = models.ForeignKey(City,
                                     on_delete=models.CASCADE,
                                     null=True)
    present_college = models.ForeignKey(College,
                                        on_delete=models.CASCADE,
                                        null=True)
    members = models.ManyToManyField(UserProfile,
                                     blank=True, null=True,  related_name='members')
    leader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='leader')
    multicity = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name + ' - ' + self.leader.mi_number

    def get_mail(self):
        return self.members.get(mi_number=self.name).email
    get_mail.short_description = 'Email'
    get_mail.admin_order_field = 'name'

class WorkshopParticipant(models.Model):
    participant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(WorkshopsEvent, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.participant.name
