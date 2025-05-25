# store/admin.py
from django.contrib import admin
from .models import Brand, Shoe

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock')
    list_filter = ('brand',)
    search_fields = ('name',)
