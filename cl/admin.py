from django.contrib import admin
from .models import ContingentLeader, Contingent, ContingentMember#, Contingent
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

def export_csv_contingent(modeladmin, request, queryset):
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
        smart_str(u"Password"),
        smart_str(u"Email"),
        smart_str(u"Mobile number"),
        smart_str(u"City"),
        smart_str(u"College"),
        smart_str(u"Contingent Strength"),
        smart_str(u"Imp?"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.cl.name),
            smart_str(obj.cl.mi_number),
            smart_str(obj.cl.fb_id),
            smart_str(obj.cl.email),
            smart_str(obj.cl.mobile_number),
            smart_str(obj.cl.present_city.city_name),
            smart_str(obj.cl.present_college.college_name),
            smart_str(obj.contingent_strength),
        ])
        for member in obj.contingent_members.all():
            writer.writerow([
                smart_str(" "),
                smart_str(member.profile.name),
                smart_str(member.profile.mi_number),
                smart_str(" "),
                smart_str(member.profile.email),
                smart_str(member.profile.mobile_number),
                smart_str(member.profile.present_city.city_name),
                smart_str(member.profile.present_college.college_name),
                smart_str(" "),
                smart_str(member.is_imp),
            ])
    return response


export_csv_contingent.short_description = u"Export CSV"

class ContingentMembersInline(admin.TabularInline):
    model = Contingent.contingent_members.through
    verbose_name = u"Member"
    verbose_name_plural = u"Members"
    extra = 0

class ContingentAdmin(admin.ModelAdmin):
    inlines = (
        ContingentMembersInline,
    )
    list_display = ('get_cl_mi_number','get_cl_pass','get_cl_name', 'get_cl_college', 'get_cl_city','contingent_strength','selected_contingent_strength','strength_alloted','is_equal','is_approved')
    readonly_fields = ('get_cl_mi_number','get_cl_pass','get_cl_name', 'get_cl_college', 'get_cl_city')
    raw_id_fields = ('cl',)
    list_filter = ['strength_alloted','is_equal','is_approved','cl__present_college__college_name']
    exclude = ['contingent_members',]
    actions = (export_csv_contingent,)

class ContingentMemberAdmin(admin.ModelAdmin):
    list_display = ('get_mi_number','get_name', 'get_email', 'get_mobile_number','is_selected','is_imp','has_paid')
    readonly_fields = ('get_mi_number','get_name', 'get_email', 'get_mobile_number')
    list_filter = ['is_selected','is_imp','has_paid']


# Register your models here.
admin.site.register(ContingentLeader, ContingentLeaderAdmin)
admin.site.register(Contingent, ContingentAdmin)
admin.site.register(ContingentMember, ContingentMemberAdmin)
