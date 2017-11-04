from django.contrib import admin
from .models import ContingentLeader, Contingent
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
        smart_str(u"Name"),
        smart_str(u"MI Number"),
        smart_str(u"Email"),
        smart_str(u"Mobile number"),
        smart_str(u"City"),
        smart_str(u"College"),
        smart_str(u"Address"),
        smart_str(u"Zip Code"),
        smart_str(u"Birthdate"),
        smart_str(u"Year of Study"),
        smart_str(u"Position of Responsibility"),
        smart_str(u"wascllastyear"),
        smart_str(u"iscrcurrently"),
        smart_str(u"timesmiattended"),
        smart_str(u"nocpiclink"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.clprofile.name),
            smart_str(obj.clprofile.mi_number),
            smart_str(obj.clprofile.email),
            smart_str(obj.clprofile.mobile_number),
            smart_str(obj.clprofile.present_city.city_name),
            smart_str(obj.clprofile.present_college.college_name),
            smart_str(obj.clprofile.postal_address),
            smart_str(obj.clprofile.zip_code),
            smart_str(obj.clprofile.dob),
            smart_str(obj.clprofile.year_of_study),
            smart_str(obj.por),
            smart_str(obj.wascllastyear),
            smart_str(obj.iscrcurrently),
            smart_str(obj.timesmiattended),
            smart_str(obj.nocpiclink),
        ])
    return response


export_csv.short_description = u"Export CSV"

class ContingentLeaderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_mi_number', 'get_college')
    list_filter = ['clprofile__present_college__college_name']
    readonly_fields = ('get_mi_number', 'get_college',)
    actions = (export_csv,)


# Register your models here.
admin.site.register(ContingentLeader, ContingentLeaderAdmin)
admin.site.register(Contingent)
