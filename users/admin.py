from django.contrib import admin
from .models import UserProfile, City, College, Group, WorkshopParticipant, CollegeList
from django.http import HttpResponse

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"Id"),
        smart_str(u"MI-numbers"),
        smart_str(u"Leader/Member's Name"),
        smart_str(u"Email"),
        smart_str(u"Mobile Number"),
        smart_str(u"College"),
        smart_str(u"City"),
        smart_str(u"Event"),
        smart_str(u"EventMI"),
        smart_str(u"Pin Code"),
        smart_str(u"Year of Study")
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.leader.mi_number),
            smart_str(obj.leader.name),
            smart_str(obj.leader.email),
            smart_str(obj.leader.mobile_number),
            smart_str(obj.present_college),
            smart_str(obj.present_city),
            smart_str(obj.event),
            smart_str(obj.eventMI),
            smart_str(obj.leader.zip_code),
            smart_str(obj.leader.year_of_study),
        ])
        for member in obj.members.all():
            writer.writerow([
                smart_str(" "),
                smart_str(member.mi_number),
                smart_str(member.name),
                smart_str(member.email),
                smart_str(member.mobile_number),
                smart_str(member.present_college),
                smart_str(member.present_city),
                smart_str(" "),
                smart_str(" "),
                smart_str(member.zip_code),
                smart_str(member.year_of_study),
            ])
    return response


export_csv.short_description = u"Export CSV"


def export_exl(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
            smart_str(u"Name"),
            smart_str(u"MI-Number"),
            smart_str(u"Email"),
            smart_str(u"CR referral code"),
            smart_str(u"Phone Number"),
            smart_str(u"College"),
            smart_str(u"Pincode"),
            smart_str(u"City"),
            smart_str(u"Gender"),
            smart_str(u"Year of Study"),
        ])
    for obj in queryset:
        writer.writerow([
                smart_str(obj.name),
                smart_str(obj.mi_number),
                smart_str(obj.email),
                smart_str(obj.cr_referral_code),
                smart_str(obj.mobile_number),
                smart_str(obj.present_college),
                smart_str(obj.zip_code),
                smart_str(obj.present_city),
                smart_str(obj.gender),
                smart_str(obj.year_of_study),
            ])
    return response

export_exl.short_description=u"Export CSV"

def checkin(modeladmin, request, queryset):
    print (queryset)
    for q in queryset:
        q.checkedin = 1
        q.save()

checkin.short_description = u"Check In"

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'present_college', 'present_city', 'checkedin')
    search_fields = ['name',
                     'present_city__city_name',
                     'present_college__college_name',
                     'mi_number']
    #list_filter = ['present_city',
    #               'present_college']

    actions = (checkin,export_exl,)


class MembersInline(admin.TabularInline):
    model = Group.members.through
    verbose_name = u"Member"
    verbose_name_plural = u"Members"
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    '''
    inlines = (
        MembersInline,
    )
    '''
    filter_horizontal = ('members',)
    list_display = ('__str__', 'leader', 'get_mail', 'mobile_number',
                    'present_college', 'present_city', 'event','eventMI')
    list_filter = ['eventMI',
                    'event',
                   'present_city__city_name',
                   'present_college__college_name']
    search_fields = ['name']
    actions = (export_csv,)
    #exclude = ("members",)


admin.site.register(City)
admin.site.register(College)
admin.site.register(CollegeList)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WorkshopParticipant)
