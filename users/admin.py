from django.contrib import admin
from .models import UserProfile, City, College, Group


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'present_college', 'present_city')
    search_fields = ['name',
                     'present_city__city_name',
                     'present_college__college_name']
    list_filter = ['present_city',
                   'present_college']


class MembersInline(admin.TabularInline):
    model = Group.members.through
    verbose_name = u"Member"
    verbose_name_plural = u"Members"
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    inlines = (
        MembersInline,
    )
    list_display = ('name', 'mobile_number',
                    'present_college', 'present_city', 'event')
    list_filter = ['event',
                   'present_city',
                   'present_college']
    search_fields = ['name']
    exclude = ("members",)


admin.site.register(City)
admin.site.register(College)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
