from django.db import models

# Create your models here.

class Url(models.Model):
	origin = models.CharField(max_length=2000)
	short = models.CharField(max_length=100, blank=True)
	def save(self, *args, **kwargs):
		if self.short == '':
			self.short = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(N));
		super(Url, self).save(*args, **kwargs)
	