from django.db import models
from modelcluster.models import ParentalKey, ClusterableModel
from wagtail.models import Orderable
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting, BaseGenericSetting
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel


# Create your models here.
@register_setting
class SocialMediaSettings(BaseGenericSetting):
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("instagram"),
        FieldPanel("twitter"),
        FieldPanel("facebook")
    ]

@register_setting
class BrandSettings(BaseGenericSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = True,
        on_delete= models.SET_NULL,
        related_name="+"
    )

    name = models.CharField(null=True, blank= True)
    copyright = models.CharField(null=True, blank= True)
    email = models.EmailField(null=True, blank= True)
    phone = models.CharField(null=True, blank= True)
    location = models.CharField(null=True, blank= True)
    schedule = models.CharField(null=True, blank= True)

    panels = [
        FieldPanel("logo"),
        FieldPanel("name"),
        FieldPanel("copyright"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("location"),
        FieldPanel("schedule"),
    ]

class MenuItem(Orderable):
    """A single item in a navigation menu."""
    link_title = models.CharField(max_length=50)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Pilih halaman internal. Kosongkan jika menggunakan link eksternal."
    )

    link_url = models.URLField(
        blank=True,
        help_text="Link eksternal (misal: https://google.com). Kosongkan jika memilih halaman internal."
    )

    show_children = models.BooleanField(
        help_text="Centang untuk menampilkan anak halaman dari 'link_page' sebagai dropdown."
    )

    page = ParentalKey("NavigationSettings", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("show_children")
    ]

    @property
    def link(self):
        return self.link_page.url if self.link_page else self.link_url

    def __str__(self):
        return self.link_title


@register_setting
class NavigationSettings(BaseSiteSetting, ClusterableModel):
    """Model to manage main site navigation."""
    class Meta:
        verbose_name = "Site Navigation"

    panels = [
        MultiFieldPanel(
            [InlinePanel("menu_items", label="Menu Item")],
            heading="Main Menu"
        ),
    ]
