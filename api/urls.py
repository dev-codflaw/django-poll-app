from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
	
	path('voter-detail/<int:pk>/', views.voter_detail, name='voter-detail'),
	path('voter-react/', views.voter, name='voter-react' ),
	path('voter-create/', views.voter_react_create, name='create-voter'),
	path('vote-register/', views.vote_register, name='vote-register'),
	path('verifier/email/<str:email>', views.get_email_verify, name='email-verifier'),

]