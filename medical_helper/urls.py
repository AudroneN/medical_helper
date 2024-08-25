"""
URL configuration for medical_helper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from medical_helper_app import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Custom registration page
    path('login/', views.custom_login, name='login'),  # Custom login page
    path('dosage/', views.dosage_view, name='dosage'),  # Dosage form page
    path('side_effects/', views.side_effect_view, name='side_effects'),  # Side effects form page
    path('notes/', views.notes_view, name='notes'),  # Notes form page
    path('send_email/', views.send_content_via_email, name='send_email'),  # Email sending page
]
