from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import *

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Address)
admin.site.register(EmergencyContact)


class BankResource(resources.ModelResource):
    class Meta:
        model = Bank


class BankAdmin(ImportExportModelAdmin):
    resource_class = BankResource

admin.site.register(Bank, BankAdmin)
