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
import re
import dns.resolver


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
					res = {'msg':'You already registered.'}
					json_data = JSONRenderer().render(res)
					return HttpResponse(json_data, content_type='application/json')
			except Exception as e:
				print('Exception:- ', e)
				serializer.save()
				res = {'msg':'You are successfully registered!'}
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
					res = {'msg':'You have already voted'}
					json_data = JSONRenderer().render(res)
					return HttpResponse(json_data, content_type='application/json')
			except Exception as e:
				print('Exception: ', e)
				# pass
				serializer.save()
				res = {'msg':'Your vote successfully submitted!'}
				json_data = JSONRenderer().render(res)
				return HttpResponse(json_data, content_type='application/json')
		else:
			json_data = JSONRenderer().render(serializer.errors)
			return HttpResponse(json_data, content_type='application/json')

	return HttpResponse({'error-1':'test'}, content_type='application/json')


def get_mx_status(domain):
	try:
		mx_record = str(dns.resolver.query(domain, 'MX')[0].exchange)
		return True
	except Exception as e:
		print(e)
		return False


@csrf_exempt
def get_email_verify(request, email):

	# Disposable Email List
	disposable_domain_list = ['mailinator.com', 'protonmail.com', 'fastmail.fm']

	# Simple Regex for syntax checking
	regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
	domain = email.split('@')[1]

	if request.method == 'GET':
		# syntax check
		verifiy_pattern = re.match(regex, email)
		if verifiy_pattern == None:
			print('Bad Syntax')
			res = {"status": "false", "error": {"code": '01', "message": "Email address invalid"}}
			json_data = JSONRenderer().render(res)
			return HttpResponse(json_data, content_type='application/json')

		elif domain in disposable_domain_list:
			res = {"status":"false","error":{"code":"02","message":"Disposable email address"}}
			json_data = JSONRenderer().render(res)
			return HttpResponse(json_data, content_type='application/json')

		elif not get_mx_status(domain):
			res = {"status":"false","error":{"code":"03","message":"Domain or MX server does not exists"}}
			json_data = JSONRenderer().render(res)
			return HttpResponse(json_data, content_type='application/json')

		else:
			res = {"status":"true","email":email, "domain": domain}
			json_data = JSONRenderer().render(res)
			return HttpResponse(json_data, content_type='application/json')

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