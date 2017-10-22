from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from sellers.models import SellerAccount

# Create your models here.

def download_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)

class Product(models.Model):
	"""docstring for Product"""
	seller = models.ForeignKey(SellerAccount)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
	media = models.ImageField(blank=True, null=True, upload_to=download_media_location )
	title = models.CharField(max_length=30)
	slug = models.SlugField(blank=True, unique=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=10000.00, null=True,)
	sale_active = models.BooleanField(default=False)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=5000.00, null=True, blank=True)

	def __str__(self):
		return self.title
		