from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from streams.blocks import body as bodyBlocks, CarouselBlock

class StandardPage(Page):
    """
    A generic content page for simple, flexible content.
    Perfect for pages like 'About Us', 'Vision & Mission', etc.
    """
    template = "content/standard_page.html"
    parent_pages_types = ["content.HomePage"]

    body = bodyBlocks

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
    parent_pages_types = ["content.HomePage"]
    subpage_types = ['content.ArticlePage']

    body = bodyBlocks

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        articles = (self.get_children().live().public().specific().order_by('-first_published_at'))

        query = request.GET.get("q")
        if query:
            articles = articles.filter(title__icontains=query)

        context["query"] = query
        context["articles"] = articles
        print(context["articles"])
        return context
    
    class Meta:
        verbose_name = "Article/News Index Page"


class ArticlePage(Page):
    """
    A single news article or announcement.
    """
    template = "content/article_page.html"
    parent_page_types = ['content.ArticleIndexPage']

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


class HomePage(Page):
    """
    The main home page model, built using a flexible StreamField
    for composing different sections.
    """
    max_count = 1
    template = "content/home_page.html"

    body = bodyBlocks

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
