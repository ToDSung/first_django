from django.contrib import admin
from .models import Board, FanPage, FacebookArticle

# Register your models here.


class FanPageAdmin(admin.ModelAdmin):
    fields = ['name']


class BoardAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(FanPage, FanPageAdmin)
admin.site.register(Board, BoardAdmin)
