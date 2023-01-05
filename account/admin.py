from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login',
                    'is_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_filter = ('date_joined', 'last_login', 'is_admin', 'is_staff',
                                                            'is_active')
    filter_horizontal = ()
    fieldsets = ()
