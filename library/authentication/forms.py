from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit
from utils.forms import CrispyHelperMixin
from .models import CustomUser, ROLE_CHOICES


class RegisterForm(CrispyHelperMixin, UserCreationForm):

    submit_label = "Registration"
    role = forms.ChoiceField(
        label="Role",
        choices=ROLE_CHOICES,
        widget=forms.Select(),
    )

    class Meta:
        model = CustomUser

        fields = (
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "role",
        )

        labels = {
            "email": "Email",
            "first_name": "Name",
            "middle_name": "Middle name",
            "last_name": "Surname",

        }

        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Name"}),
            "middle_name": forms.TextInput(attrs={"placeholder": "Middle name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Surname"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = ""
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "At least 8 symbols"}
        )
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].help_text = ""
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Confirm password"}
        )

        self._init_helper(Layout(
            Field("email"),
            Div(
                Field("first_name",  wrapper_class="col"),
                Field("middle_name", wrapper_class="col"),
                Field("last_name",   wrapper_class="col"),
                css_class="row g-2 mb-1",
            ),
            Field("role"),
            Field("password1"),
            Field("password2"),
            ButtonHolder(
                Submit("submit", self.submit_text, css_class=self.submit_css)
            ),
        ))

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = int(self.cleaned_data["role"])
        user.is_active = True
        if commit:
            user.save()
        return user


class LoginForm(CrispyHelperMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Email"
        self.fields["username"].widget = forms.EmailInput(
            attrs={"placeholder": "email@example.com", "autofocus": True}
        )
        self.fields["password"].label = "Password"
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )

        self._init_helper(Layout(
            Field("username"),
            Field("password"),
            ButtonHolder(
                Submit("submit", self.submit_text, css_class=self.submit_css)
            ),
        ))

