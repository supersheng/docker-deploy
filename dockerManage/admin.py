from django.contrib import admin
from dockerManage.models import Instance

class InstanceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print obj, form

admin.site.register(Instance)

