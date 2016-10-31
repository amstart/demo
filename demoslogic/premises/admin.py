from django.contrib import admin

from .models import Premise, CategorizationVote
#
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

class PremiseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Core', {'fields': ['subject', 'predicate', 'object', 'complement']}),
        ('Meta', {'fields': ['staged', 'user', 'pub_date']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('subject', 'predicate', 'object', 'complement', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['subject']

admin.site.register(Premise, PremiseAdmin)
admin.site.register(CategorizationVote)
