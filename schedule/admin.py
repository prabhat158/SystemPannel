from django.contrib import admin
from .models import ScheduleEvent, Check

# Register your models here.
admin.site.register(Check)
admin.site.register(ScheduleEvent) 
