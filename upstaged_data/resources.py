from import_export import resources
from .models import Voter

class VoterResource(resources.ModelResource):
    class Meta:
        model = Voter