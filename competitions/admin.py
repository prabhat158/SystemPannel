from django.contrib import admin
from .models import CompetitionsEvent, CompetitionsGenre
from users.models import Group


class GroupInline(admin.TabularInline):
    model = Group
    verbose_name = 'Group'
    verbose_name_plural = "Groups"
    exclude = ('members',)
    extra = 0


class CompetitionsEventInline(admin.ModelAdmin):
    inlines = (GroupInline,)


admin.site.register(CompetitionsGenre)
admin.site.register(CompetitionsEvent, CompetitionsEventInline)
