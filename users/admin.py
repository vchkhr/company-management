from django.contrib import admin

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    #    'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Company'), {'fields': ('company', 'office')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'company', 'office', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)
