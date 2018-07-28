from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.
class ScheduleEvent(models.Model):
    
    VENUE = ['Convocation Hall',
            'Lecture Hall Complex (LCH)',
            'LT PCSA',
            'Gymkhana Grounds',
            'NCC Grounds',
            'FC Kohli Auditorium (FCK)',
            'New Swimming Pool',
            'Kendriya Vidyalaya (KV)',
            'Student Activity Center (SAC)',
            'SJM SOM',
            'Open Air Theatre (OAT)',
            'MB Lawns',
            'Physics Parking Lot',
            'H10 T-Point',
            'PCSA Backlawns',
            'SAC Parking Lot',
            'SAC Backyard',
            'Old Swimming Pool', ]

    VENUE_CHOICES = [(c, c) for c in VENUE]

    DAY = [1,2,3,4]

    DAY_CHOICES = [(c,c) for c in DAY]

    GENRE = ['Competitions',
             'Proshows',
             'Workshops',
             'Concerts',
             'Informals',]

    GENRE_CHOICES = [(c,c) for c in GENRE]

    name = models.CharField(max_length=100,
                            blank=False)

    subtitle = models.CharField(max_length=200,
                                blank=False)

    venue = models.CharField(max_length=50,
                             choices=VENUE_CHOICES)

    description = models.TextField()

    starttime = models.CharField(max_length=4,
                                 blank = False)

    endtime = models.CharField(max_length=4,
                               blank = False) 

    day = models.IntegerField(choices = DAY_CHOICES)

    genre = models.CharField(max_length = 20,
                             choices = GENRE_CHOICES)

    def __str__(self):
        return self.name


class Check(models.Model):
    value = models.IntegerField(default=0)


@receiver(post_save, sender=ScheduleEvent)
def model_post_save(sender, **kwargs):
    t = Check.objects.get(pk=1)
    t.value +=1
    t.save()
    print(t.value)

@receiver(post_delete, sender=ScheduleEvent)
def model_post_delete(sender, **kwargs):
    t = Check.objects.get(pk=1)
    t.value +=1
    t.save()
    print(t.value)