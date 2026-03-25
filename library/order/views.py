from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages

from author.views import LibrarianRequiredMixin
from .forms import OrderCreateForm, OrderUpdateForm
from .models import Order


class OrderListView(LibrarianRequiredMixin, ListView):
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.select_related("book", "user").order_by("-created_at")


class OrderCreateView(LibrarianRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/order_form.html"
    success_url = reverse_lazy("order:order_list")

    def get_context_data(self, **kwargs):
        return super().get_context_data(page_title="Create Order", **kwargs)

    def form_valid(self, form):
        order = form.save(commit=False)
        book = order.book
        if book.count <= 0:
            messages.error(self.request, "This book is out of stock.")
            return self.form_invalid(form)
        book.count -= 1
        book.save()
        order.save()
        messages.success(self.request, "Order created successfully.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)


class OrderUpdateView(LibrarianRequiredMixin, UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = "order/order_form.html"
    success_url = reverse_lazy("order:order_list")

    def get_context_data(self, **kwargs):
        return super().get_context_data(page_title="Edit Order", **kwargs)

    def form_valid(self, form):
        order = self.get_object()
        new_end_at = form.cleaned_data.get("end_at")

        # If end_at is being set for the first time → return book
        if new_end_at and order.end_at is None:
            order.book.count += 1
            order.book.save()

        messages.success(self.request, "Order updated successfully.")
        return super().form_valid(form)


class OrderDeleteView(LibrarianRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("order:order_list")

    def post(self, request, *args, **kwargs):
        order = self.get_object()

        # If the book hasn't been returned yet, restore count
        if order.end_at is None:
            order.book.count += 1
            order.book.save()

        messages.success(request, f"Order #{order.pk} deleted.")
        return super().post(request, *args, **kwargs)
