from django.urls import path

from .views import (DesktopView, DesktopUpdateDeleteApiView, MobileView, MobileUpdateDeleteApiView, OverallView, OverallUpdateDeleteApiView)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('desktop/', DesktopView.as_view()),
    path('desktop/<int:pk>/', DesktopUpdateDeleteApiView.as_view()),
    path('mobile/', MobileView.as_view()),
    path('mobile/<int:pk>/', MobileUpdateDeleteApiView.as_view()),
    path('performance/', OverallView.as_view()),
    path('performance/<int:pk>/', OverallUpdateDeleteApiView.as_view()),
]