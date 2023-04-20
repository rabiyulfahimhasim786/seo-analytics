from django.db import models

# Create your models here.

class Pageperformance(models.Model):
    input_url = models.URLField(max_length = 255)
    output_data = models.TextField(max_length = 255)

class MobilePageperformance(models.Model):
    mobile_url = models.URLField(max_length = 255)
    mobile_data = models.TextField(max_length = 255)