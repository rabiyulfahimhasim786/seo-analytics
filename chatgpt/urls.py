from django.urls import path
from .views import (ChatView, PdfUpdateDeleteApiView)
from . import views

urlpatterns = [
    path('chatgpt/', views.chatgptindex, name='chatgptindex'),
    path('chat/', ChatView.as_view()),
    path('chat/<int:pk>/', PdfUpdateDeleteApiView.as_view()),
]

