from django import template

register = template.Library()

@register.inclusion_tag("tags/main_menu.html", takes_context=True)
def main_menu(context, menu_type="desktop"):
    """
    Retrieves the main menu from the settings context.
    """
    # settings.global.NavigationSettings should be available in the context
    # because of the 'wagtail.contrib.settings.context_processors.settings'
    settings = context.get("settings")
    navigation_settings = getattr(settings, 'global', {}).get('NavigationSettings')

    return {
        "menu_items": navigation_settings.menu_items.all() if navigation_settings else [],
        "request": context.get("request"),
        "menu_type": menu_type,
    }
