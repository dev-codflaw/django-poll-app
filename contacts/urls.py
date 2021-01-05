from django.urls import path

from rest_framework import routers, serializers, viewsets
from contacts.views import ContactViewSet, LabelViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'labels', LabelViewSet)

app_name = 'contacts'

urlpatterns = [
    # path('', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    # path('contacts/', ,name='contacts'),
]

urlpatterns += router.urls
