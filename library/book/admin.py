from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html

from .models import Book


class AvailabilityFilter(admin.SimpleListFilter):
    title = 'Availability'
    parameter_name = 'availability'

    def lookups(self, request, model_admin):
        return (
            ('available', '✅ In Stock'),
            ('out',       '❌ Out of Stock'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'available':
            return queryset.filter(count__gt=0)
        if self.value() == 'out':
            return queryset.filter(count=0)
        return queryset


class AuthorInline(admin.TabularInline):
    from author.models import Author
    model = Book.authors.through
    extra = 1
    verbose_name = 'Author'
    verbose_name_plural = 'Book Authors'


class BookOrderInline(admin.TabularInline):
    from order.models import Order
    model = Order
    extra = 0
    fields = ('user', 'created_at', 'end_at', 'plated_end_at', 'is_returned')
    readonly_fields = ('user', 'created_at', 'end_at', 'is_returned')
    show_change_link = True
    verbose_name = 'Order'
    verbose_name_plural = 'Checkout History'

    @admin.display(description='Returned')
    def is_returned(self, obj):
        if obj.plated_end_at:
            return format_html(
                '<span style="color:#27ae60">✔ {}</span>',
                obj.plated_end_at.strftime('%Y-%m-%d')
            )
        return format_html('<span style="color:#e74c3c">On Hand</span>')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').order_by(
            'plated_end_at',
            '-created_at',
        )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'authors_list', 'count_badge',
        'total_orders', 'active_orders',
    )
    list_display_links = ('id', 'name')
    list_filter = (
        AvailabilityFilter,
        ('authors', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('name', 'description', 'authors__name', 'authors__surname')
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        ('General Data', {
            'description': 'These fields are set when the book is added and generally do not change.',
            'fields': ('name', 'description'),
        }),
        ('Dynamic Data (Inventory)', {
            'description': 'Fields in this section are automatically updated when orders are created and closed.',
            'fields': ('count',),
        }),
    )

    inlines = (AuthorInline, BookOrderInline)

    @admin.display(description='Authors', ordering='authors__surname')
    def authors_list(self, obj):
        authors = obj.authors.all()
        if not authors:
            return format_html('<span style="color:#aaa">—</span>')
        return ', '.join(f'{a.name} {a.surname}' for a in authors)

    @admin.display(description='Copies', ordering='count')
    def count_badge(self, obj):
        if obj.count > 0:
            color = '#27ae60'
            icon = '✅'
        else:
            color = '#e74c3c'
            icon = '❌'
        return format_html(
            '{} <strong style="color:{}">{}</strong>',
            icon, color, obj.count,
        )

    @admin.display(description='Total Checkouts')
    def total_orders(self, obj):
        return obj.order_count

    @admin.display(description='Currently On Hand')
    def active_orders(self, obj):
        n = obj.active_order_count
        if n:
            return format_html(
                '<span style="color:#e67e22;font-weight:600">{}</span>', n
            )
        return format_html('<span style="color:#aaa">0</span>')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('authors').annotate(
            order_count=Count('order', distinct=True),
            active_order_count=Count(
                'order',
                filter=Q(order__plated_end_at__isnull=True),
                distinct=True,
            ),
        )