from django.contrib import admin
from .models import ArtsAndIdeasGenre, ArtsAndIdeasEvent

# Register your models here.
admin.site.register(ArtsAndIdeasEvent)
admin.site.register(ArtsAndIdeasGenre)
