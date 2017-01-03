from django.contrib import admin

from .models import Argument, ArgumentVote
#
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

class ArgumentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Core', {'fields': ['sentence', 'premise1', 'premise2', 'premise3',
                             'conclusion', 'premise1_if', 'premise2_if', 'aim']}),
        ('Meta', {'fields': ['staged', 'user', 'pub_date']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('premise1', 'premise2', 'conclusion', 'aim', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['conclusion']

admin.site.register(Argument, ArgumentAdmin)
admin.site.register(ArgumentVote)
