from django.contrib import admin
from .models import ProshowsGenre, ProshowsEvent

admin.site.register(ProshowsEvent)
admin.site.register(ProshowsGenre)
