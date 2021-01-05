from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from upstaged_data.models import VoterReact, Vote
from api.serializers import VoterReactSerializer, VoteSerializer
from rest_framework.decorators import api_view

from django.core import serializers
from django.http import HttpResponse
import io
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt


def voter(request):
	voters = VoterReact.objects.all()
	print(list(voters))
	serialized_obj = serializers.serialize('json', voters)
	return HttpResponse(serialized_obj) 
	# return JsonResponse(list(serialized_obj))



def voter_detail(request, pk):
	voter = VoterReact.objects.get(id = pk)
	serializer = VoterReactSerializer(voter)
	if serializer.is_valid:
		json_data = JSONRenderer().render(serializer.data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		return HttpResponse(serializer.errors, content_type='application/json')


@csrf_exempt
def voter_react_create(request):
	if request.method == 'POST':
		json_data = request.body
		print('json data:-', json_data)

		stream = io.BytesIO(json_data)
		# print('stream:-', stream)

		python_data = JSONParser().parse(stream)
		print('json parse python data:-', python_data)

		serializer = VoterReactSerializer(data=python_data)


		if serializer.is_valid():
			print('serializer-data:-', serializer.validated_data)
			try:
				if VoterReact.objects.get(email=serializer.validated_data.get('email')):
					res = {'msg':'User Already Exist'}
					json_data = JSONRenderer().render(res)
					return HttpResponse(json_data, content_type='application/json')
			except Exception as e:
				print('Exception:- ', e)
				serializer.save()
				res = {'msg':'New User Created'}
				json_data = JSONRenderer().render(res)
				return HttpResponse(json_data, content_type='application/json')
		else:
			json_data = JSONRenderer().render(serializer.errors)
			return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def vote_register(request):
	if request.method == 'POST':
		json_data = request.body
		print('json data:-', json_data)

		stream = io.BytesIO(json_data)
		# print('stream:-', stream)

		python_data = JSONParser().parse(stream)
		print('json parse python data:-', python_data)

		serializer = VoteSerializer(data=python_data)


		if serializer.is_valid():
			# print('serializer-data:-', serializer.data)
			print('serializer-data:-', serializer.validated_data)
			print(serializer.validated_data.get('email'))
			# print(serializer.data['email'])
			try:
				if Vote.objects.get(email=serializer.validated_data.get('email')):
					res = {'msg':'Already Voted'}
					json_data = JSONRenderer().render(res)
					return HttpResponse(json_data, content_type='application/json')
			except Exception as e:
				print('Exception: ', e)
				# pass
				serializer.save()
				res = {'msg':'Data Created'}
				json_data = JSONRenderer().render(res)
				return HttpResponse(json_data, content_type='application/json')
		else:
			json_data = JSONRenderer().render(serializer.errors)
			return HttpResponse(json_data, content_type='application/json')

	return HttpResponse({'error-1':'test'}, content_type='application/json')


@api_view(['GET', 'PUT'])
def voter_create(request, name, email):
    try:
    	voter = VoterReact(name=name, email=email)
        # tutorial = Tutorial.objects.get(pk=pk) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'Exception': 'error'}) 
 
  #   if request.method == 'GET':
  #   	voter.save()
	 #    serialized_obj = serializers.serialize('json', voter)
		# return HttpResponse(serialized_obj) 
 
  #   elif request.method == 'PUT': 
  #       tutorial_data = JSONParser().parse(request) 
  #       tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
  #       if tutorial_serializer.is_valid(): 
  #           tutorial_serializer.save() 
  #           return JsonResponse(tutorial_serializer.data) 
  #       return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    


# @api_view(['GET', 'POST'])
# def voter(request):
#     if request.method == 'GET':
#         voters = VoterReact.objects.all()
        
#         name = request.query_params.get('name', None)
#         if name is not None:
#             voters = voters.filter(name__icontains=name)
        
#         voter_serializers = VoterReactSerializer(voters, many=True)
#         return JsonResponse(voter_serializers.data, safe=False)
#         # 'safe=False' for objects serialization
 
#     elif request.method == 'POST':
#         voters_data = JSONParser().parse(request)
#         voter_serializers = VoterReactSerializer(data=voters_data)
#         if voter_serializers.is_valid():
#             voter_serializers.save()
#             return JsonResponse(voter_serializers.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(voter_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         count = VoterReact.objects.all().delete()
#         return JsonResponse({'message': '{} Voter were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
#  