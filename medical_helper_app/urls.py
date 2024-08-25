from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('dosage/', views.dosage_view, name='dosage'),
    path('side_effects/', views.side_effect_view, name='side_effects'),
    path('notes/', views.notes_view, name='notes'),
    path('send_email/', views.send_content_via_email, name='send_email'),
]
