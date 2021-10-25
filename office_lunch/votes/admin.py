from django.contrib import admin

from .models import Vote, Winner


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_date', 'menu', 'user')
    ordering = ('-id',)
    readonly_fields = ('get_date',)

    def get_date(self, obj):
        return obj.menu.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'menu__date'


class WinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'menu', 'vote_count', )
    ordering = ('-id',)
    readonly_fields = ('date',)


admin.site.register(Vote, VoteAdmin)
admin.site.register(Winner, WinnerAdmin)
