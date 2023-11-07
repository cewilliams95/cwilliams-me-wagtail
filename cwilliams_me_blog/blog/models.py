from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index

class BlogListing(Page):
    """ Lists all pages, TODO later: list category of posts """
    custom_title = models.CharField(
        max_length=100,
        blank=True,
        null=False
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title')
    ]
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context
class BlogPost(Page):

    # Database fields
    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]


    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]


    # Parent page / subpage type rules

    parent_page_types = ['BlogListing']
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPost, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
