from django.contrib import admin
from dockerManage.models import Instance

class InstanceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print obj, form
        obj.port = 1234
        obj.save()

    def delete_model(self, request, obj):
        print obj.port
        obj.delete()
admin.site.register(Instance, InstanceAdmin)

