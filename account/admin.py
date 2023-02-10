from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'last_login',
                    'is_admin', 'is_staff', 'is_active', 'date_joined',)
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_filter = ('last_login', 'is_admin',
                   'is_staff', 'date_joined', 'is_active')
    filter_horizontal = ()
    fieldsets = ()
