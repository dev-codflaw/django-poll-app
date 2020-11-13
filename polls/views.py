from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from .models import Choice, Question, Vote
from django.views.generic import TemplateView, View


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """ 
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # login_url = '/login/'
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     max_votes = Choice.objects.aggregate(Max('votes'))['votes__max']
    #     return Choice.objects.get(votes=max_votes)

def results(request, question_id):
    if(Vote.objects.filter(question_id=question_id)):
        pass
    else:
        messages.info(request, "something is wrong!")
        return redirect('index')

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def vote(request, question_id):
    if(Vote.objects.filter(question_id=question_id, user_id=request.user)):
        messages.info(request, 'You have already voted!')
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        vote = Vote()
        vote.user = request.user
        vote.question_id = question_id
        vote.choice_id = request.POST['choice']
        vote.is_voted = 1
        vote.save()

        choice_obj = Choice.objects.get(pk=request.POST['choice'])
        choice_obj.votes = choice_obj.votes+1
        choice_obj.save() 

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))



def bracket(request):
    # if request.POST['bracket-id']:
    return render(request, 'polls/bracket.html', {'data':'hello world'})
    
    # return render(request, 'polls/bracket.html')


class Bracket(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'polls/brackets.html', {'data':'Please enter bracket ID'})
    
    def post(self, request, *args, **kwargs):
        return render(request, 'polls/brackets.html', {'data':request.POST['bracket-id']})