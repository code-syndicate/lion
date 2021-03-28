"""lion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/u
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from config import admin_site1

urlpatterns = [
    path('bank-admin/', admin_site1.urls ),
    path( "", include('banking.urls') )
]+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)