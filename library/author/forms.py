from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit
from .models import Author


class AuthorForm(forms.ModelForm):

    class Meta:
        model  = Author
        fields = ("surname", "name", "patronymic")
        widgets = {
            "surname":    forms.TextInput(attrs={"placeholder": "Enter surname..."}),
            "name":       forms.TextInput(attrs={"placeholder": "Enter name..."}),
            "patronymic": forms.TextInput(attrs={"placeholder": "Enter patronymic (optional)..."}),
        }

    def __init__(self, *args, **kwargs):
        submit_text = kwargs.pop("submit_text", "Save Author")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"novalidate": True}
        self.helper.layout = Layout(
            Field("surname"),
            Field("name"),
            Field("patronymic"),
            ButtonHolder(
                Submit("submit", "Save Author", css_class="btn btn-success w-100")
            ),
        )