from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from .forms import AuthorForm
from .models import Author


class LibrarianRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("authentication:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.is_librarian:
            messages.error(request, "Access denied. Librarian rights required.")
            return redirect("book:list")

        return super().dispatch(request, *args, **kwargs)


class AuthorListView(LibrarianRequiredMixin, ListView):
    model                = Author
    template_name        = "author/author_list.html"
    context_object_name  = "authors"

    def get_queryset(self):
        return (
            Author.objects
            .annotate(book_count=Count("books"))
            .order_by("surname", "name")
        )


class AuthorCreateView(LibrarianRequiredMixin, CreateView):
    model         = Author
    form_class    = AuthorForm
    template_name = "author/author_form.html"
    success_url   = reverse_lazy("author:author_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["submit_text"] = "Create author"
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(page_title="New author", **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Author created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)


class AuthorUpdateView(LibrarianRequiredMixin, UpdateView):
    model         = Author
    form_class    = AuthorForm
    template_name = "author/author_form.html"
    success_url   = reverse_lazy("author:author_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["submit_text"] = "Save changes"
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(page_title="Edit author", **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Author updated successfully.")
        return super().form_valid(form)


class AuthorDeleteView(LibrarianRequiredMixin, DeleteView):
    model         = Author
    success_url   = reverse_lazy("author:author_list")

    def post(self, request, *args, **kwargs):
        author = self.get_object()

        if author.books.exists():
            messages.error(
                request,
                f"Cannot delete '{author.surname}': author has books attached."
            )
            return redirect("author:author_list")

        messages.success(request, f"Author '{author.surname}' deleted.")
        return super().post(request, *args, **kwargs)