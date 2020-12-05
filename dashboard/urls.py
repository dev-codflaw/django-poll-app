from django.urls import path

from dashboard.views import Dashboard, TestDashboard

from django.views.generic import TemplateView
from dashboard.views import date_wise_vote_list, redirect_dashboard_link
from django.contrib.auth.decorators import login_required


app_name = 'dashboard'

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    path('dashboard/', redirect_dashboard_link, name='dashboard'),
    path('voting/dashboard/', login_required(Dashboard.as_view()), name='voting-dashboard'),
    path('voting/dashboard/test/', login_required(TestDashboard.as_view()), name='test-voting-dashboard'),
    path('votes/date-wise/', login_required(date_wise_vote_list), name='date-wise-votes'),

    path('thank-you/', TemplateView.as_view(template_name='dashboard/thank-you.html'), name='thank-you'),

]