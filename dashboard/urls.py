from django.urls import path

from dashboard.views import Dashboard

from django.views.generic import TemplateView


app_name = 'dashboard'

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),

]