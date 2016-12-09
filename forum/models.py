from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from assets.models import Asset
from django.conf import settings

class Subject(models.Model):

    name = models.CharField(max_length=255)
    asset_id = models.ForeignKey(Asset)
    description = HTMLField(blank=True)
    image = models.ImageField(upload_to='forum_images', blank=True, null=True)

    def __unicode__(self):
        return "%s | %s | %s" % (self.id, self.name, self.asset_id.asset_display_name)


class Thread(models.Model):

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='threads')
    subject = models.ForeignKey(Subject, related_name='threads')
    created_at = models.DateTimeField(default=timezone.now)
    num_views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Post(models.Model):

    thread = models.ForeignKey(Thread, related_name='posts')
    comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.comment