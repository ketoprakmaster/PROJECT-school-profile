from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from streams.blocks import BodyContentBlock, CarouselBlock

class StandardPage(Page):
    """
    A generic content page for simple, flexible content.
    Perfect for pages like 'About Us', 'Vision & Mission', etc.
    """
    template = "content/standard_page.html"
    parent_pages_types = ["content.HomePage"]

    body = StreamField(BodyContentBlock(),use_json_field=True, blank=True, null=True)

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

    body = StreamField(BodyContentBlock(),use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = (self.get_children().live().public().specific().order_by('-first_published_at'))

        query = request.GET.get("query")
        page = request.GET.get("page",1)

        if query:
            posts = posts.filter(title__icontains=query)

        paginator = Paginator(posts,10)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["query"] = query
        context["posts"] = posts
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
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = RichTextField(null=True,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('thumbnail'),
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

    body = StreamField(BodyContentBlock(),use_json_field=True, blank=True, null=True)


    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
