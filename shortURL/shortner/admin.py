from shortner.models import *
from django.contrib import admin

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('code', 'url', 'expiry_date')

admin.site.register(ShortURL, ShortURLAdmin)