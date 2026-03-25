from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .decorators import librarian_required
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    template_name = "authentication/register.html"
    form_class    = RegisterForm
    success_url   = reverse_lazy("authentication:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("book:list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # super() вызывает form.save() автоматически
        messages.success(self.request, "Registration successful! Log in.")
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    form_class                  = LoginForm
    template_name               = "authentication/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        messages.success(
            self.request,
            f"Welcome, {user.first_name or user.email}!"
        )
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("authentication:login")

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


@librarian_required
def user_list_view(request):
    librarians = CustomUser.objects.filter(role=1).order_by('-is_active', 'id')
    readers = CustomUser.objects.filter(role=0).order_by('-is_active', 'id')

    context = {
        'librarians': librarians,
        'readers': readers
    }

    return render(request, 'authentication/user_list.html', context)


@login_required(login_url='authentication:login')
def user_detail_view(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if not request.user.is_librarian and request.user.id != target_user.id:
        messages.error(request, "You do not have permission to view someone else's profile.")
        return redirect('book:list')

    return render(request, 'authentication/user_detail.html', {'target_user': target_user})