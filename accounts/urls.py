from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import LoginView, RegisterView, Hello
from .import views

urlpatterns = [
    path('hello/', Hello.as_view(), name='hello'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),        
]

