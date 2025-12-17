from wagtail.documents.models import AbstractDocument, Document
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model
from wagtail.models import Page
from wagtail.fields import StreamField

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models

from streams.blocks import BodyContentBlock

class BookResource(AbstractDocument):
    author = models.CharField(max_length=255, blank=True)
    date_published = models.DateField(blank=True, null=True)

    cover_image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    admin_form_fields = Document.admin_form_fields + (
        'author',
        'date_published',
        'cover_image',
    )

class LibraryIndexPage(Page):
    template = "library/library-index-page.html"
    parent_pages_types = ["content.StandardPage"]

    body = StreamField(BodyContentBlock(),use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Get all resources, potentially filtering by search query
        resources = BookResource.objects.all().order_by('-date_published')
        query = request.GET.get("query")
        page = request.GET.get("page",1)

        if query:
            resources = resources.filter(title__icontains=query)

        paginator = Paginator(resources,10)

        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)

        context["query"] = query
        context['resources'] = resources

        return context
