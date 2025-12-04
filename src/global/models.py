from django.db import models

from wagtail.contrib.settings.models import  register_setting, BaseGenericSetting
from wagtail.admin.panels import FieldPanel


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
    description = models.CharField(null=True, blank= True)

    panels = [
        FieldPanel("logo"),
        FieldPanel("name"),
        FieldPanel("copyright"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("location"),
        FieldPanel("schedule"),
        FieldPanel("description")
    ]
