from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models

from streams.blocks import BodyContentBlock

class BookResource(models.Model):
    file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date_published = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('author'),
        FieldPanel('file'),
        FieldPanel('date_published'),
        FieldPanel('cover_image'),
    ]

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.file.title if self.file else "Untitled Book"

    class Meta:
        ordering = ['date_published']

class LibraryIndexPage(Page):
    template = "library/library-index-page.html"
    parent_pages_types = ["content.StandardPage"]

    body = StreamField(BodyContentBlock(),use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_pagination(self, request, resources):
        page = request.GET.get("page",1)

        paginator = Paginator(resources,10)

        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)

        return resources

    def get_context(self, request):
        context = super().get_context(request)
        resources = BookResource.objects.all()
        query = request.GET.get("query")

        if query:
            resources = resources.filter(title__icontains=query)

        resources = self.get_pagination(request, resources)

        context["query"] = query
        context['resources'] = resources

        return context
