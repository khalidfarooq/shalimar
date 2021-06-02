from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('upload',model_form_upload,name="upload"),
]
