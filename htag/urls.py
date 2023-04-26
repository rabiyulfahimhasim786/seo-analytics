from django.urls import path
from .views import (TagView, TagUpdateDeleteApiView)
from . import views
# from .views import CustomChatView

urlpatterns = [
    path('', views.index,  name='index'),
    path('tag/', TagView.as_view()),
    path('tag/<int:pk>/', TagUpdateDeleteApiView.as_view()),
]
