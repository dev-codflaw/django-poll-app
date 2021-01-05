from rest_framework import serializers
from upstaged_data.models import VoterReact, Vote

class VoterReactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    email =  serializers.CharField(max_length=50)
    is_valid = serializers.BooleanField(default=False)
    source = serializers.CharField(max_length=30, default='added by api')

    def create(self, validate_data):
    	return VoterReact.objects.create(**validate_data)
	# class Meta:
	# 	model = VoterReact
	# 	# field = ('id',
	# 	# 		'name',
	# 	# 		'email',
	# 	# 		'is_valid')
	# 	field = '__all__'



class VoteSerializer(serializers.Serializer):
	game = serializers.CharField(max_length=30)
	voted_for = serializers.CharField(max_length=30)
	email = serializers.CharField(max_length=50)

	def create(self, validate_data):
		return Vote.objects.create(**validate_data)