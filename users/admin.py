from django.contrib import admin
from .models import UserProfile, City, College, Group


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'present_college', 'present_city')
    search_fields = ['name', 'present_college', 'present_city']


admin.site.register(City)
admin.site.register(College)
admin.site.register(Group)
admin.site.register(UserProfile, UserProfileAdmin)
