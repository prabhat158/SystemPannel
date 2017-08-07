from django.contrib import admin
from .models import CompetitionsEvent, CompetitionsGenre

admin.site.register(CompetitionsGenre)
admin.site.register(CompetitionsEvent)
