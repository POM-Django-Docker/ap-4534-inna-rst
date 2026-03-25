from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Order


class OrderStatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('open',   'Open'),
            ('closed', 'Closed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'open':
            return queryset.filter(plated_end_at__isnull=True)
        if self.value() == 'closed':
            return queryset.filter(plated_end_at__isnull=False)
        return queryset


class OverdueFilter(admin.SimpleListFilter):
    title = 'Overdue Status'
    parameter_name = 'overdue'

    def lookups(self, request, model_admin):
        return (
            ('yes', '🔴 Overdue'),
            ('no',  '🟢 On Time'),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        now = timezone.now()
        if self.value() == 'yes':
            return queryset.filter(
                plated_end_at__isnull=True,
                end_at__lt=now,
            )
        if self.value() == 'no':
            return queryset.filter(
                plated_end_at__isnull=True,
                end_at__gte=now,
            )
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_link', 'book_link',
        'created_at', 'end_at', 'plated_end_at', 'status_badge',
    )
    list_display_links = ('id',)
    list_filter = (
        OrderStatusFilter,
        OverdueFilter,
        ('book',  admin.RelatedOnlyFieldListFilter),
        ('user',  admin.RelatedOnlyFieldListFilter),
        'created_at',
    )
    search_fields = (
        'book__name', 'user__email', 'user__first_name', 'user__last_name',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 30

    fieldsets = (
        ('Static Data', {
            'description': 'Set during order creation and do not change.',
            'fields': ('user', 'book', 'created_at'),
        }),
        ('Checkout Data (dynamic)', {
            'description': 'Return date is populated when the order is closed.',
            'fields': ('end_at', 'plated_end_at'),
        }),
    )
    readonly_fields = ('created_at',)

    @admin.display(description='User')
    def user_link(self, obj):
        url = reverse('admin:authentication_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    @admin.display(description='Book')
    def book_link(self, obj):
        url = reverse('admin:book_book_change', args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.name)

    @admin.display(description='Status')
    def status_badge(self, obj):
        from django.utils import timezone
        if obj.plated_end_at:
            return format_html(
                '<span style="background:#d5f5e3;color:#1e8449;padding:2px 8px;'
                'border-radius:10px;font-size:11px">✔ Returned</span>'
            )
        if obj.end_at and obj.end_at < timezone.now():
            return format_html(
                '<span style="background:#fadbd8;color:#922b21;padding:2px 8px;'
                'border-radius:10px;font-size:11px">Overdue</span>'
            )
        return format_html(
            '<span style="background:#fef9e7;color:#7d6608;padding:2px 8px;'
            'border-radius:10px;font-size:11px">On Hand</span>'
        )

    actions = ['close_selected_orders']

    @admin.action(description='✅ Close selected orders (mark as returned)')
    def close_selected_orders(self, request, queryset):
        from django.utils import timezone

        open_orders = queryset.filter(plated_end_at__isnull=True)

        count = open_orders.update(plated_end_at=timezone.now())

        self.message_user(request, f'Successfully closed {count} order(s).')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'book')