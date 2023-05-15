from rest_framework import serializers
from .models import Sitemapapi

class SitemapapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitemapapi
        fields = ('id', 'xmls', 'brokenlinks', 'workinglinks')