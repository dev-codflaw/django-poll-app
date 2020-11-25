from django.urls import path

from .views import Bracket, TournamentList, ParticipantList
from . import views
from django.views.generic import TemplateView


app_name = 'polls'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.TemplateView.as_view(template_name='polls/home.html'), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:pk>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('<int:question_id>/is_voted/', views.vote, name='is_voted'),

    path('bracket/', views.bracket, name='bracket'),
    path('brackets/', Bracket.as_view(), name='brackets'),

    path('tournaments/', TournamentList.as_view(), name='tournaments'),
    path('participants/', ParticipantList.as_view(), name='participants'),
]