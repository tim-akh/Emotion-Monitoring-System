from django.shortcuts import render, HttpResponseRedirect, redirect
import cv2
import numpy as np
import tensorflow as tf
import os
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .camera import VideoCamera
from fer_stats.models import Record
import pytz

from django.http import StreamingHttpResponse


@login_required
def index_view(request):
    context = {}
    return render(request, "emotion_recognition/index.html", context)

@login_required
def emotion_recognition_view(request):
    context = {}
    return render(request, 'emotion_recognition/emotion_recognition.html', context)


@login_required
def video_feed_view(request):
    return StreamingHttpResponse(gen(VideoCamera(req=request)),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
