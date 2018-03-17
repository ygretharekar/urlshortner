from django.db import models

# Create your models here.


class URLShortner(models.Model):
	short_id = models.SlugField(max_length=8, primary_key=True)
	url = models.URLField(max_length=200)
	count = models.IntegerField(default=0)


	def __str__(self):
		return self.url


