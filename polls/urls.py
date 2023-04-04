from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sitemap/', views.sitemap_xml_data, name='sitemap_xml_data'),
    path('metatag/', views.metatag, name='metatag'),
    path('content/', views.content, name='content'),
]
