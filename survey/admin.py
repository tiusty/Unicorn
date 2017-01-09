from django.contrib import admin
from survey.models import RentingSurveyModel, RentingDesintations

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class RentingSurveyModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    readonly_fields = ("created",)
    inlines = [ChoiceInline]
    fieldsets = (
        (None, {'fields': ('name', 'userProf')}),
        ('Survey', {'fields': ('home_type', 'minPrice', 'maxPrice',)}),
        ('Created', {'fields': ('created',)}),
    )
    list_display = ('name', 'userProf','get_short_name', )
    list_filter = ['userProf']
    search_fields = ('name',)

class AddressInLine(admin.StackedInline):
    model = RentingDesintations


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)