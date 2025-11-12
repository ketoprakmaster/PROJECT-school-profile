from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class StandardPage(Page):
    """
    A generic content page for simple, flexible content.
    Perfect for pages like 'About Us', 'Vision & Mission', etc.
    """
    template = "content/standard_page.html"

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow")),
        ('image', ImageChooserBlock(icon="image")),
    ], use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Standard Page"


class ArticleIndexPage(Page):
    """
    Page to list all its children ArticlePages.
    """
    template = "content/article_index_page.html"
    subpage_types = ['content.ArticlePage'] # Restrict children to be ArticlePage

    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Get all live, public child pages, ordered by most recent date
        articles = self.get_children().live().public().order_by('-first_published_at')
        context['articles'] = articles
        return context

    class Meta:
        verbose_name = "Article/News Index Page"


class ArticlePage(Page):
    """
    A single news article or announcement.
    """
    template = "content/article_page.html"
    parent_page_types = ['content.ArticleIndexPage'] # Can only be created under an ArticleIndexPage

    date = models.DateField("Post date")
    introduction = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow")),
        ('image', ImageChooserBlock(icon="image")),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('introduction'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Article/News Page"