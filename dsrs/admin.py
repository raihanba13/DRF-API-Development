from django.contrib import admin
from .models import Territory, Currency, DSR, Resource
from pprint import pprint

# Register your models here.
admin.site.register(Territory)
admin.site.register(Currency)
# admin.site.register(DSR)
admin.site.register(Resource)


def delete_dsr_resource(modeladmin, request, queryset):
    print(queryset)

    dsr_id_delete = []
    territory_id_delete = []
    currecny_id_delete = []

    for x in queryset:
        dsr_id_delete.append(x.id)
        territory_id_delete.append(x.currency_id)
        currecny_id_delete.append(x.territory_id)
    print(dsr_id_delete)
    print(dsr_id_delete)
    print(dsr_id_delete)
    '''
    on_delete=models.CASCADE
    This should delete everything.
    But as my less experience in ORM, I will do it manually
    '''
    DSR.objects.filter(id__in=dsr_id_delete).delete()
    Currency.objects.filter(id__in=currecny_id_delete).delete()
    Territory.objects.filter(id__in=territory_id_delete).delete()
    Resource.objects.filter(dsrs_id__in=dsr_id_delete).delete()

    # breakpoint()
    # queryset.update(status='p')

delete_dsr_resource.short_description = "Delete selected DSR and their Resources"

class DSRAdmin(admin.ModelAdmin):
    actions = [delete_dsr_resource]

admin.site.register(DSR, DSRAdmin)
