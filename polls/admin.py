from django.contrib import admin

from .models import Premise, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PremiseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['text']
    votes = ['votes']

admin.site.register(Premise, PremiseAdmin)
