from django.contrib import admin
from .models import ConcertsGenre, ConcertsEvent

admin.site.register(ConcertsGenre)
admin.site.register(ConcertsEvent)
