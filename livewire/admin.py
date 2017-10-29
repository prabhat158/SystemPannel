from django.contrib import admin
from .models import LivewireBand
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
        smart_str(u"Band Name"),
        smart_str(u"Facebook Link"),
        smart_str(u"Manager"),
        smart_str(u"Email"),
        smart_str(u"Phone Number"),
        smart_str(u"Band Members"),
        smart_str(u"Hometown"),
        smart_str(u"Preferred City"),
        smart_str(u"Original Composition"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.band_name),
            smart_str(obj.facebook_link),
            smart_str(obj.manager),
            smart_str(obj.emailid),
            smart_str(obj.mobile_number),
            smart_str(obj.bandmembers),
            smart_str(obj.hometown),
            smart_str(obj.preferred_city),
            smart_str(obj.original_composition),
        ])
    return response


export_csv.short_description = u"Export CSV"


class LivewireBandAdmin(admin.ModelAdmin):
    list_display = ('band_name', 'preferred_city',)
    list_filter = ('preferred_city',)
    actions = (export_csv,)


admin.site.register(LivewireBand, LivewireBandAdmin)
