from django.db import models

# Create your models here.
# from django.db import models

class Tag(models.Model):
    url = models.URLField()
    output = models.TextField()