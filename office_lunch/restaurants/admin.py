from django.contrib import admin

from .models import Restaurant, Menu


class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', )
    ordering = ('-id',)


class MenuAdmin(admin.ModelAdmin):
    search_fields = ('cuisine',)
    list_display = ('id', 'date', 'cuisine', 'restaurant', )
    ordering = ('-id',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
