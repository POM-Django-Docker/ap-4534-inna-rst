from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class OrderInline(admin.TabularInline):
    from order.models import Order
    model = Order
    extra = 0
    fields = ('book', 'created_at', 'end_at', 'plated_end_at', 'status_badge')
    readonly_fields = ('created_at', 'end_at', 'status_badge')
    show_change_link = True

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.plated_end_at:
            return format_html(
                '<span style="color:#27ae60;font-weight:600">✔ Returned</span>'
            )
        return format_html(
            '<span style="color:#e67e22;font-weight:600"> On Hand</span>'
        )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'full_name', 'role_badge',
        'is_active_icon', 'is_staff', 'created_at',
    )
    list_display_links = ('id', 'email')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    ordering = ('-created_at',)
    list_per_page = 25

    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'middle_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',),
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'middle_name', 'last_name',
                'role', 'password1', 'password2', 'is_active',
            ),
        }),
    )

    USERNAME_FIELD = 'email'
    inlines = (OrderInline,)

    @admin.display(description='Full Name', ordering='last_name')
    def full_name(self, obj):
        parts = filter(None, [obj.last_name, obj.first_name, obj.middle_name])
        return ' '.join(parts) or '—'

    @admin.display(description='Role')
    def role_badge(self, obj):
        if obj.role == 1:
            return format_html(
                '<span style="background:#f39c12;color:#fff;padding:2px 8px;'
                'border-radius:10px;font-size:11px">Librarian</span>'
            )
        return format_html(
            '<span style="background:#3498db;color:#fff;padding:2px 8px;'
            'border-radius:10px;font-size:11px">Reader</span>'
        )

    @admin.display(description='Active', boolean=True)
    def is_active_icon(self, obj):
        return obj.is_active

    actions = ['activate_users', 'deactivate_users']

    @admin.action(description='✅ Activate selected users')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Successfully activated {updated} user(s).')

    @admin.action(description='❌ Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Successfully deactivated {updated} user(s).')