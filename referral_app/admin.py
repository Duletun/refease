from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

class UserAdmin(BaseUserAdmin):
    # Форма для добавления и изменения пользователей в админке
    list_display = ('phone_number', 'invite_code', 'activated_invite_code', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('invite_code', 'activated_invite_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
