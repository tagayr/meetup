from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.http import Http404

from .models import Question, Choice

# Create your views here.


def index(request):
    # return HttpResponse("Hello, welcome to the poll's index.")
    # what we actually want to do is return the 5 last questions
    latest_questions_list = Question.objects.order_by('-pub_date')[:5]
    '''
    template = loader.get_template('polls/index.html')
    context = {
        'latest_questions_list': latest_questions_list
    }
    return HttpResponse(template.render(context, request))

    '''
    context = {'latest_questions_list': latest_questions_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # response = "You're looking at the question %s."
    # return HttpResponse(response % question_id)
    '''
    try:
        # select question
        question = Question.objects.get(pk=question_id)
    except:
        # raise Http404 exception
        raise Http404("Question does not exist")
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # response = "You are looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


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

















