from django.shortcuts import render

# Create your views here.

from contacts.models import Contacts, Label
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets


class ListContacts(APIView):
	def get(self, request, format=None):
		names = [Contact.name for contact in Contacts.objects.all()]
		return Response(names)




# Serializers define the API representation.
class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'first_name', 'last_name', 'email', 'contact_number',]
        # fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer



# Serializers define the API representation.
class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'description', 'color', 'status']
        # fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer