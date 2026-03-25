from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit
from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ("name", "description", "count", "authors")
        widgets = {
            "name":        forms.TextInput(attrs={"placeholder": "Enter book title..."}),
            "description": forms.Textarea(attrs={"placeholder": "Enter description...", "rows": 4}),
            "count":       forms.NumberInput(attrs={"placeholder": "Number of copies", "min": 0}),
            "authors":     forms.SelectMultiple(),
        }
        labels = {
            "name": "Title",
            "description": "Description",
            "count": "Copies in stock",
            "authors": "Authors",
        }

    def __init__(self, *args, **kwargs):
        submit_text = kwargs.pop("submit_text", "Save Book")
        super().__init__(*args, **kwargs)
        self.fields["authors"].required = False
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"novalidate": True}
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            Field("count"),
            Field("authors"),
            ButtonHolder(
                Submit("submit", submit_text, css_class="btn btn-success w-100")
            ),
        )
