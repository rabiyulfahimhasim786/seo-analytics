from django.db import models

# Create your models here.

class Sitemapapi(models.Model):
    xmls = models.URLField(max_length = 255)
    brokenlinks = models.TextField(blank=True)
    workinglinks = models.TextField(blank=True)