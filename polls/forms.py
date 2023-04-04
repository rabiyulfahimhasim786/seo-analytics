from django import forms

from . models import Sitemapxml


class SitemapxmlForm(forms.ModelForm):
    class Meta:
        model = Sitemapxml
        fields = ('url',)