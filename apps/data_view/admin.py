from django.contrib import admin

# Register your models here.
from django.urls import reverse,reverse_lazy
from .models import PerDataCount

admin.site.site_header = "可视化管理后台"

@admin.register(PerDataCount)
class DataViewAdmin(admin.ModelAdmin):
    fields = ['dataNum','dataBase','year']
    search_fields = ['dataBase']
    # list_display_links = ()
    # list_display = ('dataNum','dataBase','year')
    # list_editable = ('dataNum', 'available')