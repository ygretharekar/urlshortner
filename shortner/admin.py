from django.contrib import admin

# Register your models here.

from .models import URLShortner


@admin.register(URLShortner)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'url', 'count')
    fields = ['short_id', 'url', 'count']
