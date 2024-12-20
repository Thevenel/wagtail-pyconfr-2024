from django.db import models
from job.models import JobPage

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


from wagtail.admin.panels import (
    MultiFieldPanel,
    FieldPanel
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting
)

class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "+",
        help_text = "Homepage image"
    )
    hero_text = models.CharField(max_length=255, help_text="Make the home stand out")
    hero_cta = models.CharField(
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Add a CTA text`"
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null = True,
        blank = True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the CTA"
    )
    feature_section_title = models.CharField(max_length=100, null=True, blank=True)
    features = StreamField(
        [
            ('feature_icon', ImageChooserBlock(required=False)),
            ('feature_title', blocks.CharBlock(required=True)),
            ('feature_desc', blocks.CharBlock(required=True))
        ],
        
        null = True,
        blank = True
    )
    def get_context(self, request):
        context = super().get_context(request)
        context['jobs'] = JobPage.objects.live().order_by('-first_published_at')
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel (
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                MultiFieldPanel (
                    [
                        FieldPanel("hero_cta"),
                        FieldPanel("hero_cta_link")
                    ]
                )
                
            ],
            heading = "Hero section"
        ),
        FieldPanel("feature_section_title"),
        FieldPanel("features")
    ]

@register_setting
class NavigationSettings(BaseGenericSetting):
    linkedin_url = models.URLField(verbose_name="Linkedin URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    mastodon_url = models.URLField(verbose_name="Mastodon URL", blank=True)
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("linkedin_url"),
                FieldPanel("github_url"),
                FieldPanel("mastodon_url")
            ],
            "Social settings"
        )
    ]
    

