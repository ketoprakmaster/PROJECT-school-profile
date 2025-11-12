from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from content import blocks


class HomePage(Page):
    """
    The main home page model, built using a flexible StreamField
    for composing different sections.
    """
    template = "home/home_page.html"

    body = blocks.body

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
