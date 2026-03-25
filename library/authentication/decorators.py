from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def librarian_required(view_func=None, login_url='book:list'):
    actual_decorator = user_passes_test(
        lambda user: user.is_authenticated and user.is_librarian,
        login_url=login_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator