from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Color


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color_preview')
    list_editable = ('name',)
    list_per_page = 20
