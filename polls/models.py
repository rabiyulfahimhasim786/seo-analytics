from django.db import models

# Create your models here.
from django.db import models

class Sitemapxml(models.Model):
    url = models.URLField(blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.url