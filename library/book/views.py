from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages

from author.views import LibrarianRequiredMixin
from .forms import BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "book/list.html"
    context_object_name = "books"

    def get_queryset(self):
        return Book.objects.prefetch_related("authors").all()


class BookCreateView(LibrarianRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "book/book_form.html"
    success_url = reverse_lazy("book:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["submit_text"] = "Create Book"
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(page_title="New Book", **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Book created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)


class BookUpdateView(LibrarianRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "book/book_form.html"
    success_url = reverse_lazy("book:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["submit_text"] = "Save Changes"
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(page_title="Edit Book", **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Book updated successfully.")
        return super().form_valid(form)


class BookDeleteView(LibrarianRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("book:list")

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        if book.order_set.filter(end_at__isnull=True).exists():
            messages.error(
                request,
                f"Cannot delete '{book.name}': book has active orders."
            )
            return redirect("book:list")

        messages.success(request, f"Book '{book.name}' deleted.")
        return super().post(request, *args, **kwargs)
