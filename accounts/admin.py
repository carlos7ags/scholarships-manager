from import_export import resources
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib import admin


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
