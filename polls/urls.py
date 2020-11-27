from django.urls import path

from django.views.generic import TemplateView


app_name = 'polls'
urlpatterns = [
    path('s/', TemplateView.as_view(template_name='polls/home.html'), name='home'),
  
]