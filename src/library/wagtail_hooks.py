from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from .models import BookResource

class LibraryViewSet(SnippetViewSet):
    model = BookResource
    icon = "doc-full"  # Use a relevant icon from the Wagtail icon library
    menu_label = "Pustaka"  # The text displayed in the menu
    menu_name = "Library"  # A unique name for the menu item
    menu_order = 300  # An integer to determine the menu item's order
    add_to_admin_menu = True  # Key setting to add it to the main sidebar menu


# Register the viewset instead of the model directly with register_snippet()
register_snippet(LibraryViewSet)
