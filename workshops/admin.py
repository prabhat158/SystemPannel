from django.contrib import admin
from .models import WorkshopsGenre, WorkshopsEvent

admin.site.register(WorkshopsEvent)
admin.site.register(WorkshopsGenre)
