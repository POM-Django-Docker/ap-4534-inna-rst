from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from .models import Author


class AuthorBookInline(admin.TabularInline):
    from book.models import Book
    model = Author.books.through
    extra = 1
    verbose_name = 'Book'
    verbose_name_plural = 'Author Books'
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'patronymic', 'books_count', 'books_preview')
    list_display_links = ('id', 'full_name')
    search_fields = ('name', 'surname', 'patronymic')
    ordering = ('surname', 'name')
    list_per_page = 25
    list_filter = (
        ('books', admin.RelatedOnlyFieldListFilter),
    )

    fieldsets = (
        (' Author Info', {
            'description': 'Author details — set during creation and do not change.',
            'fields': ('surname', 'name', 'patronymic'),
        }),
    )

    inlines = (AuthorBookInline,)

    @admin.display(description='Author', ordering='surname')
    def full_name(self, obj):
        return f'{obj.surname} {obj.name}'

    @admin.display(description='Books Count', ordering='books_count')
    def books_count(self, obj):
        n = obj.books_count
        if n == 0:
            return format_html('<span style="color:#aaa">0</span>')
        return format_html('<strong>{}</strong>', n)

    @admin.display(description='Books Preview')
    def books_preview(self, obj):
        books = obj.books.all()[:3]
        if not books:
            return format_html('<span style="color:#aaa">—</span>')

        html_links = format_html_join(
            ', ',
            '<a href="{}">{}</a>',
            ((reverse('admin:book_book_change', args=[b.id]), b.name) for b in books)
        )

        if obj.books_count > 3:
            suffix = format_html(' <span style="color:#aaa">and others</span>')
            return format_html('{}{}', html_links, suffix)

        return html_links

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('books').annotate(
            books_count=Count('books', distinct=True)
        )