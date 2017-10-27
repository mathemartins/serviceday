from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class SellerAccount(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="manager_sellers", blank=True)
	# token = token-generator
	active = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return reverse("products:vendor_detail", kwargs={"vendor_name": self.user.username})


def artisan_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)

class ArtisanAccount(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	job_title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	image = models.ImageField(blank=True, null=True, upload_to='artisan_media_location')
	# token = token-generator
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.user.username)
