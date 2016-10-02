from django.contrib import admin

from .models import Premise, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PremiseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['subject']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('subject', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['subject']
    votes = ['votes']

admin.site.register(Premise, PremiseAdmin)
