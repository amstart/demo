from django.contrib import admin

from . import models
#
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

class PremiseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Core', {'fields': ['sentence']}),
        ('Meta', {'fields': ['staged', 'user', 'pub_date']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('sentence', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['sentence']

admin.site.register(models.Premise, PremiseAdmin)
admin.site.register(models.PremiseVote)
admin.site.register(models.Noun)
admin.site.register(models.Verb)
admin.site.register(models.Adjective)
