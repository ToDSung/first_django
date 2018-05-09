from django.contrib import admin
from .models import FanPage, Article

# Register your models here.


class FanPageAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(FanPage, FanPageAdmin)
