from django.urls import path

from .views import (Overallapi, OverallapiUpdateDeleteApiView, SitemapapiView)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('brokenlinks/', SitemapapiView.as_view(), name="SitemapapiView"),
    path('site/', Overallapi.as_view(), name="site"),
    path('site/<int:pk>/', OverallapiUpdateDeleteApiView.as_view(), name="OverallapiUpdateDeleteApiView"),
]