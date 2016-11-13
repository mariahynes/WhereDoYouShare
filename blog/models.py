from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
from assets.models import Asset

class Post(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    asset_ID = models.ForeignKey(Asset)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    num_views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title

