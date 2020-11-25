from django.urls import path
from django.conf.urls import url
from .import views
from memail.views import SimpleEmailView

app_name = 'memail'

urlpatterns = [
    path('memail/', SimpleEmailView.as_view(), name='email'),

    url(r'^image_load/$', views.image_load, name='image_load'),
    # path('image_load/', views.image_load, name='image_load'),

]