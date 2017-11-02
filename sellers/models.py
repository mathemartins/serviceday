from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify


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


class ArtisanCategoryQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ArtisanCategoryManager(models.Manager):
	def get_queryset(self):
		return ArtisanCategoryQuerySet(self.model, using=self._db)

	def all(self):
		return super(ArtisanCategoryManager, self).all(*args, **kwargs)

class ArtisanCategory(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	artisan_account = models.ManyToManyField(ArtisanAccount)
	active = models.BooleanField(default=True)

	objects = ArtisanCategoryManager()

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		view_name = "artisan_category:detail"
		return reverse(view_name, kwargs={"slug": self.slug})

def artisan_category_pre_save_receiver(sender, instance, *args, **kwargs):
	instance.title = instance.title.lower()
	if not instance.slug:
		instance.slug = slugify(instance.title)
		
pre_save.connect(artisan_category_pre_save_receiver, sender=ArtisanCategory)