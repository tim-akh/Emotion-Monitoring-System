from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('emotion_recognition', views.emotion_recognition_view, name='emotion_recognition'),
    path('video_feed', views.video_feed_view, name='video_feed')
]