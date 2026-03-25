from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class CrispyHelperMixin:
    submit_text: str = "Submit"
    submit_css:  str = "btn btn-primary w-100"

    def _init_helper(self, layout: Layout) -> None:
        self.helper              = FormHelper()
        self.helper.form_method  = "post"
        self.helper.attrs        = {"novalidate": True}
        self.helper.layout       = layout