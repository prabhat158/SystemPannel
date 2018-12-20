from django.contrib import admin
from .models import ContingentLeader, Contingent, ContingentMember, College, Visits#, Contingent
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
        smart_str(u"City in cl form"),
        smart_str(u"College in cl form"),
        smart_str(u"City"),
        smart_str(u"College"),
        smart_str(u"Address"),
        smart_str(u"Zip Code"), 
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
            smart_str(obj.city),
            smart_str(obj.college),
            smart_str(obj.clprofile.present_city.city_name),
            smart_str(obj.clprofile.present_college.college_name),
            smart_str(obj.clprofile.postal_address),
            smart_str(obj.clprofile.zip_code),
            smart_str(obj.clprofile.year_of_study),
            smart_str(obj.por),
            smart_str(obj.wascllastyear),
            smart_str(obj.iscrcurrently),
            smart_str(obj.timesmiattended),
            smart_str(obj.nocpiclink),
        ])
    return response

export_csv.short_description = u"Export CSV"

def approve_contingent(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_approved=1
        obj.save()
approve_contingent.short_description=u"Approve Contingent"

def export_paid_list(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=paid.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"CL"),
        smart_str(u"Male Strength"),
        smart_str(u"Female Strength"),
    ])
    for obj in queryset:
        m_count=0
        f_count=0
        for mem in obj.contingent_members.all():
            if((mem.gender=="Male")and(mem.has_paid==1)):
                m_count+=1
            elif((mem.gender=="Female")and(mem.has_paid==1)):
                f_count+=1
        writer.writerow([
            smart_str(obj.cl.mi_number),
            smart_str(m_count),
            smart_str(f_count)
        ])
    return response
export_paid_list.short_description = u"Export Paid List"

def export_csv_college(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=college.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"picode")
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.name),
            smart_str(obj.pin_code)
        ])
    return response
export_csv_college.short_description = u"Export College CSV"

def export_csv_visitor(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=visitors.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"MI Number"),
        smart_str(u"Email"),
        smart_str(u"Pin Code"),
        smart_str(u"Gender")
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.visitor.mi_number),
            smart_str(obj.visitor.email),
            smart_str(obj.pin_code),
            smart_str(obj.gender),
        ])
    return response
export_csv_visitor.short_description = u"Export visitor CSV"

def add_and_export_contingent(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    for obj in queryset:
        college=College(name=obj.college, pin_code=obj.clprofile.zip_code)
        college.save()
        contingent = Contingent(cl=obj.clprofile, college=college)
        contingent.save()
        writer.writerow([
            smart_str(contingent.cl.name),
            smart_str(contingent.cl.mi_number),
            smart_str(contingent.cl.google_id),
            smart_str(contingent.cl.email),
            smart_str(contingent.cl.mobile_number),
            smart_str(contingent.cl.present_city.city_name),
            smart_str(college.name),
            smart_str(college.pin_code),
            ])
    return response
add_and_export_contingent.short_description = u"Make Contingent"


class VisitorAdmin(admin.ModelAdmin):
    list_display=('__str__', 'pin_code')
    actions = (export_csv_visitor,)

class CollegeAdmin(admin.ModelAdmin):
    list_display=('__str__', 'pin')
    actions = (export_csv_college,)
    

class ContingentLeaderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_mi_number', 'get_college')
    list_filter = ['clprofile__present_college__college_name']
    readonly_fields = ('get_mi_number', 'get_college',)
    actions = (export_csv, add_and_export_contingent)

def export_csv_members(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=members.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"MI Number"),
        smart_str(u"Email"),
        smart_str(u"Selected"),
        smart_str(u"IMP"),
        smart_str(u"Aproved"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.profile.name),
            smart_str(obj.profile.mi_number),
            smart_str(obj.profile.email),
            smart_str(obj.is_selected),
            smart_str(obj.is_imp),
            smart_str(obj.cl_approve)
        ])
    return response
export_csv_members.short_description = u"Export Members"


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
        smart_str(u"Pin Code"),
        smart_str(u"Contingent Strength"),
        smart_str(u"Male Strength"),
        smart_str(u"Female Strength"),
        smart_str(u"Alloted Strength"),
        smart_str(u"Male Alloted"),
        smart_str(u"Female Alloted"),
        smart_str(u"Imp?"),
        smart_str(u"Gender"),
        smart_str(u"CL Aprove"),
        smart_str(u"Selected"),
        smart_str(u"CL MI"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.cl.name),
            smart_str(obj.cl.mi_number),
            smart_str(obj.cl.google_id),
            smart_str(obj.cl.email),
            smart_str(obj.cl.mobile_number),
            smart_str(obj.cl.present_city.city_name),
            smart_str(obj.college.name),
            smart_str(obj.college.pin_code),
            smart_str(obj.contingent_strength),
            smart_str(obj.m_strength),
            smart_str(obj.f_strength),
            smart_str(obj.strength_alloted),
            smart_str(obj.male_alloted),
            smart_str(obj.fem_alloted),
        ])
        allot_male_num = 0
        allot_fem_num = 0
        for member in obj.contingent_members.all():
            if (member.gender=="Male"):
                allot_male_num += 1
            else:
                allot_fem_num += 1 
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
                smart_str(" "),
                smart_str(" "),
                smart_str(" "),
                smart_str(" "),
                smart_str(" "),
                smart_str(" "),
                smart_str(member.is_imp),
                smart_str(member.gender),
                smart_str(member.cl_approve),
                smart_str(member.is_selected),
                smart_str(obj.cl.mi_number),
            ])
        writer.writerow([
            smart_str(obj.pk),
            smart_str(u"Male Requests:"),
            smart_str(allot_male_num),
            smart_str(u"Female Requests:"),
            smart_str(allot_fem_num)
            ])
    return response


export_csv_contingent.short_description = u"Export CSV"

def approve_contingent(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_approved=1
        obj.save()
approve_contingent.short_description = u"Approve Contingent"

class ContingentMembersInline(admin.TabularInline):
    model = Contingent.contingent_members.through
    verbose_name = u"Member"
    verbose_name_plural = u"Members"
    extra = 0

class ContingentAdmin(admin.ModelAdmin):
    '''inlines = (
        ContingentMembersInline,
    )'''
    list_display = ('get_cl_mi_number','get_cl_pass','get_cl_name', 'get_cl_college', 'get_cl_city','contingent_strength','selected_contingent_strength','strength_alloted','is_equal','is_approved')
    readonly_fields = ('get_cl_mi_number','get_cl_pass','get_cl_name', 'get_cl_college', 'get_cl_city')
    raw_id_fields = ('cl',)
    list_filter = ['strength_alloted','is_equal','is_approved','cl__present_college__college_name']
    exclude = ['contingent_members',]
    actions = (export_csv_contingent, approve_contingent, export_paid_list,)
    search_fields=['cl__mi_number']

class ContingentMemberAdmin(admin.ModelAdmin):
    list_display = ('get_mi_number','get_name', 'get_email', 'get_mobile_number','is_selected','is_imp','has_paid')
    readonly_fields = ('get_mi_number','get_name', 'get_email', 'get_mobile_number')
    list_filter = ['is_selected','is_imp','has_paid','cl_approve','gender']
    search_fields = ['profile__mi_number']
    actions = (export_csv_members,)


# Register your models here.
admin.site.register(Visits, VisitorAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(ContingentLeader, ContingentLeaderAdmin)
admin.site.register(Contingent, ContingentAdmin)
admin.site.register(ContingentMember, ContingentMemberAdmin)
