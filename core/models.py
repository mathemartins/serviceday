from django.db import models

# Create your models here.

class BannerContentControl(models.Model):
	text_header = models.CharField(max_length=99, default="Happy New Year", blank=True, null=True)
	text_head_button = models.CharField(max_length=99, default="Coming Soon!!", blank=True, null=True)
	content_statement = models.CharField(max_length=99, blank=True, null=True)

	def __str__(self):
		return self.text_header

