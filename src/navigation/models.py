"""Improved Menus models with ordering and better structure."""
from django.db import models
from django.urls import reverse, NoReverseMatch
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.snippets.models import register_snippet
from wagtail.models import Page, Orderable


class MenuItem(Orderable):
    """A single item within a Menu. Supports hierarchy and ordering."""

    page = ParentalKey(
        "Menu",
        related_name="menu_items",
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
        help_text="Leave blank to make this a top-level menu item.",
    )

    link_title = models.CharField(max_length=50, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(
        help_text="Open link in a new browser tab.",
    )

    panels = [
        FieldPanel("link_title"),
        MultiFieldPanel(
            [
                PageChooserPanel("link_page"),
                FieldPanel("link_url"),
            ],
            heading="Link",
        ),
        FieldPanel("open_in_new_tab"),
        FieldPanel("parent"),
    ]

    @property
    def title(self):
        """Display title, falling back to page title or placeholder."""
        if self.link_page and not self.link_title:
            return self.link_page.title
        return self.link_title or "Missing Title"

    @property
    def href(self):
        """Determine the final URL for this menu item."""
        if self.link_page:
            return self.link_page.get_url()

        if self.link_url:
            try:
                return reverse(self.link_url)
            except NoReverseMatch:
                return self.link_url

        return "#"

    def __str__(self):
        return self.title


@register_snippet
class Menu(ClusterableModel):
    """A reusable and reorderable menu snippet."""

    title = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=255,
        verbose_name="slug",
        allow_unicode=True,
        unique=True,
        help_text="A unique slug to identify this menu.",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Items", heading="Menu structure"),
    ]

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def top_level_items(self):
        """Return only top-level menu items, ordered properly."""
        return self.menu_items.filter(parent__isnull=True).order_by("sort_order")

    def get_nested_items(self):
        """Return a nested list/dict structure of the menu hierarchy."""
        def build_tree(parent=None):
            items = (
                self.menu_items.filter(parent=parent).order_by("sort_order")
            )
            return [
                {
                    "item": item,
                    "children": build_tree(item),
                }
                for item in items
            ]

        return build_tree()
