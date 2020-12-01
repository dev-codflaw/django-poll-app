from import_export import resources
from .models import Voter

class PersonResource(resources.ModelResource):
    class Meta:
        model = Voter