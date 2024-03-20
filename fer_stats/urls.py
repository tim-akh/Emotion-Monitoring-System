from django.urls import path
from . import views


urlpatterns = [
    path('fer_stats', views.fer_stats_view, name='fer_stats')
]