from __future__ import unicode_literals
import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.


# upload directory and folder name instance
def upload_dir(instance, filename):
	return "%s/%s" %(instance.id, filename)

class ArtisanAccount(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="manager_artisans", blank=True)
	banner_image = ProcessedImageField(upload_to=upload_dir, processors=[ResizeToFill(500, 200)], format='JPEG', options={'quality':100}, null=True, blank=True)
	image = ProcessedImageField(upload_to=upload_dir, processors=[ResizeToFill(250, 150)], format='JPEG', options={'quality':100}, null=True, blank=True)
	address = models.CharField(max_length=300)
	mobile_number = models.CharField(max_length=11)
	active = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return reverse("skill:vendor_detail", kwargs={"vendor_name": self.user.username})
