from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.http import Http404
from django.views import generic


from .models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form, i.e. detail
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Please select a choice to vote.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always return an HttpResponseRedirect after successfully dealing with POST data.
        # Things might go south if the user hits the Back button
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

















