# Django Imports
from django.contrib import admin

# zip-code imports
from commutes.models import ZipCodeBase, ZipCodeChild, CommuteType


class ZipCodeDictionaryChildInLine(admin.StackedInline):
    model = ZipCodeChild
    extra = 0


class ZipCodeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ZipCodes',
         {'fields': ['zip_code', ]}),
    ]
    list_display = ('zip_code',)
    search_fields = ['zip_code']
    # noinspection SpellCheckingInspection
    inlines = [ZipCodeDictionaryChildInLine]


class CommuteTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Commute Type',
         {'fields': ['commute_type',]})
    ]
    list_display = ('commute_type',)


admin.site.register(ZipCodeBase, ZipCodeAdmin)
admin.site.register(CommuteType, CommuteTypeModelAdmin)