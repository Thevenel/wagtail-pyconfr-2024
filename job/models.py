from django.db import models
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from django.utils import timezone

from taggit.models import TaggedItemBase

class JobListing(Page):
    intro = RichTextField()
    
    content_panels = Page.content_panels + [
        FieldPanel("intro")
    ]
    
    def get_context(self, request):
        # Update context to include all live JobPage instances
        context = super().get_context(request)
        context['jobs'] = JobPage.objects.live()  # Fetch all published JobPage objects
        return context

class JobPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'JobPage', 
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )
    
class JobTagIndexPage(Page):
 
    def get_context(self, request):
        #filter by tag
        tag = request.GET.get('tag')
        jobs = JobPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['jobs'] = jobs
        return context
        
        
class JobPage(Page):
    date = models.DateField("Published Date", default=timezone.now)
    location = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, help_text="Max 200 characters")
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Choose a image for your cover"
    )
    salary = models.IntegerField(verbose_name="A salary approximation")
    company = models.CharField(max_length=200)
    tags = ClusterTaggableManager(through=JobPageTag, blank=True)
    content = StreamField(
        [
            ('heading', blocks.CharBlock(form_classname='full title', template='blocks/heading.html')),
            ('paragraph', blocks.RichTextBlock(template='blocks/paragraph.html')),
            ('blockquote', blocks.BlockQuoteBlock(template='blocks/blockquote.html')),
            ('list', blocks.ListBlock(blocks.CharBlock(), template='blocks/list.html')),
            ('html', blocks.RawHTMLBlock(template='blocks/html.html')),
            ('image', ImageChooserBlock())
        ],
        null=True, 
        blank=True
        
    )
    
    def get_context(self, request):
        context = super().get_context(request)
        context['jobs'] = JobPage.objects.live().order_by('-first_published_at')
        return context
    
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("location"),
        FieldPanel("short_description"),
        FieldPanel("thumbnail"),
        FieldPanel("salary"),
        FieldPanel("company"),
        FieldPanel("content"),
        FieldPanel("tags"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('location'),
        index.SearchField('company'),
    ]