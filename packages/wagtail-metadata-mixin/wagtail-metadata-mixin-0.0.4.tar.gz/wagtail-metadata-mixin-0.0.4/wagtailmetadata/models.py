# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page, Site
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from meta import settings as meta_settings
from meta_mixin.models import ModelMeta


class MetadataMixin(ModelMeta):
    context_meta_name = 'meta'

    use_og = meta_settings.USE_OG_PROPERTIES
    use_use_title_tag = meta_settings.USE_TITLE_TAG

    object_type = None
    custom_namespace = None

    _metadata_default = {
        'use_og': 'use_og',
        'use_title_tag': 'use_title_tag',

        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
        'url': 'get_meta_url',

        'object_type': 'get_meta_object_type',
        'site_name': 'get_meta_site_name',

        'twitter_card': 'get_meta_twitter_card',
        'twitter_author': 'get_author_twitter',
        'twitter_site': meta_settings.TWITTER_SITE,

        'gplus_author': 'get_author_gplus',
        'gplus_publisher': meta_settings.GPLUS_PUBLISHER,

        'og_author': 'get_author_url',
        'og_publisher': meta_settings.FB_PUBLISHER,

        'facebook_app_id': meta_settings.FB_APPID,
        'fb_pages': meta_settings.FB_PAGES,

        'published_time': 'published_time',
        'modified_time': 'latest_revision_created_at',
        'expiration_time': 'expire_at',

        'locale': 'get_meta_locale',
        'custom_namespace': 'get_meta_custom_namespace',

        'get_domain': 'get_domain',
    }

    def get_domain(self):
        request = self.get_request()
        if request and getattr(request, 'site', None):
            return request.site.hostname

        site = self.get_site()
        if site is not None:
            return site.hostname

        if not meta_settings.SITE_DOMAIN:
            raise ImproperlyConfigured('META_SITE_DOMAIN is not set')
        return meta_settings.SITE_DOMAIN

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_keywords(self):
        return []

    def get_meta_image(self):
        if bool(meta_settings.DEFAULT_IMAGE) is True:
            return self.build_absolute_uri(meta_settings.DEFAULT_IMAGE)
        return None

    def get_meta_url(self):
        return self.build_absolute_uri(self.url)

    def get_meta_object_type(self):
        return self.object_type or meta_settings.SITE_TYPE

    def get_meta_site_name(self):
        request = self.get_request()
        if request and getattr(request, 'site', None):
            if bool(request.site.site_name) is True:
                return request.site.site_name

        site = self.get_site()
        if site is not None:
            if bool(site.site_name) is True:
                return site.site_name

        return settings.WAGTAIL_SITE_NAME

    def get_meta_twitter_card(self):
        if self.get_meta_image() is not None:
            return 'summary_large_image'
        return 'summary'

    def get_meta_locale(self):
        return getattr(settings, 'LANGUAGE_CODE', 'en_US')

    def get_meta_custom_namespace(self):
        return self.custom_namespace or meta_settings.OG_NAMESPACES

    def get_author(self):
        author = super(MetadataMixin, self).get_author()
        author.fb_url = meta_settings.FB_AUTHOR_URL
        author.twitter_profile = meta_settings.TWITTER_AUTHOR
        author.gplus_profile = meta_settings.GPLUS_AUTHOR
        author.get_full_name = self.owner.get_full_name
        return author

    def build_absolute_uri(self, url):
        request = self.get_request()
        if request is not None:
            return request.build_absolute_uri(url)

        if url.startswith('http'):
            return url

        site = self.get_site()
        if site is not None:
            return '%s%s' % (site.root_url, url if url.startswith('/') else '/' + url)

        raise NotImplementedError

    @property
    def published_time(self):
        return self.go_live_at or self.first_published_at

    def get_context(self, request):
        context = super(MetadataMixin, self).get_context(request)
        context[self.context_meta_name] = self.as_meta(request)
        return context


class MetadataPageMixin(MetadataMixin, models.Model):

    search_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        ImageChooserPanel('search_image'),
    ]

    def get_meta_image(self):
        if self.search_image is not None:
            return self.build_absolute_uri(
                self.search_image.get_rendition('fill-800x450').url)
        return super(MetadataPageMixin, self).get_meta_image()

    class Meta:
        abstract = True
