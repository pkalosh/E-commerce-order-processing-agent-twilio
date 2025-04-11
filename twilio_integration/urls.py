from django.urls import path
from . import views

urlpatterns = [
    path('sms-webhook/', views.sms_webhook, name='sms_webhook'),
    path('voice-webhook/', views.voice_webhook, name='voice_webhook'),
    path('voice-intent/', views.voice_intent, name='voice_intent'),
]