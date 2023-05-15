from rest_framework import serializers
from .models import Pageperformance, MobilePageperformance, Overallperformance

class PageperformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pageperformance
        fields = ('id', 'input_url', 'output_data')


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobilePageperformance
        fields = ('id', 'mobile_url', 'mobile_data')


class OverallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overallperformance
        fields = ('id', 'urls', 'mobile', 'desktop')