from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','status' ,'is_admin', 'is_staff','last_login','date_registered')
    search_fields = ('email', 'first_name', 'last_name', )
    readonly_fields = ('email',)
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets =  ()

admin.site.register(Account, AccountAdmin)