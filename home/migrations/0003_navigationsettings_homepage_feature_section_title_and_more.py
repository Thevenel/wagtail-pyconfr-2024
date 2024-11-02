# Generated by Django 5.0.9 on 2024-11-01 19:04

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin_url', models.URLField(blank=True, verbose_name='Linkedin URL')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub URL')),
                ('mastodon_url', models.URLField(blank=True, verbose_name='Mastodon URL')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='feature_section_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='features',
            field=wagtail.fields.StreamField([('feature_icon', 0), ('feature_title', 1), ('feature_desc', 1)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 1: ('wagtail.blocks.CharBlock', (), {'required': True})}, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_cta',
            field=models.CharField(default='Test', help_text='Add a CTA text`', max_length=255, verbose_name='Hero CTA'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_cta_link',
            field=models.ForeignKey(blank=True, help_text='Choose a page to link to for the CTA', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Hero CTA link'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_text',
            field=models.CharField(default='test', help_text='Make the home stand out', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Homepage image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]