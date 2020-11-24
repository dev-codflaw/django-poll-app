from django.urls import path

from .views import Bracket
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),


]