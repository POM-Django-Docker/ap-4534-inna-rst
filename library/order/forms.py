from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit

from authentication.models import CustomUser
from book.models import Book
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ("book", "user", "plated_end_at")
        widgets = {
            "book":          forms.Select(),
            "user":          forms.Select(),
            "plated_end_at": forms.DateTimeInput(
                attrs={"type": "datetime-local", "placeholder": "Planned return date"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        labels = {
            "book": "Book",
            "user": "Reader",
            "plated_end_at": "Planned return date",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(count__gt=0)
        self.fields["user"].queryset = CustomUser.objects.filter(role=0, is_active=True)
        self.fields["plated_end_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"novalidate": True}
        self.helper.layout = Layout(
            Field("book"),
            Field("user"),
            Field("plated_end_at"),
            ButtonHolder(
                Submit("submit", "Create Order", css_class="btn btn-success w-100")
            ),
        )


class OrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ("plated_end_at", "end_at")
        widgets = {
            "plated_end_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        labels = {
            "plated_end_at": "Planned return date",
            "end_at": "Actual return date",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plated_end_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_at"].required = False
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"novalidate": True}
        self.helper.layout = Layout(
            Field("plated_end_at"),
            Field("end_at"),
            ButtonHolder(
                Submit("submit", "Save Changes", css_class="btn btn-success w-100")
            ),
        )
