# menus/templatetags/menu_tags.py
from django import template
from ..models import Menu

register = template.Library()

@register.simple_tag
def main_menu(menu_slug):
    """
    Returns a structured list of menu items for the given menu slug.
    Usage:
        {% main_menu "main" as menu %}
    """
    try:
        menu = Menu.objects.prefetch_related("menu_items__link_page").get(slug=menu_slug)
        all_items = menu.menu_items.all()

        # Map of ID -> item
        item_dict = {item.id: item for item in all_items}

        # Initialize children and attach to parents
        for item in all_items:
            item.children_list = []
        for item in all_items:
            if item.parent_id in item_dict:
                item_dict[item.parent_id].children_list.append(item)

        # Mark items with children
        for item in all_items:
            item.has_child = bool(item.children_list)

        # Only top-level items
        top_level_items = [i for i in all_items if i.parent_id is None]

    except Menu.DoesNotExist:
        top_level_items = []

    return {"menu_items": top_level_items}
