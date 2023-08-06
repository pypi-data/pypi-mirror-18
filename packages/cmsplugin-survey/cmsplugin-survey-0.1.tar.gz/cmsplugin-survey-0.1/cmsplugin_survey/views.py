from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Answer, Vote

def vote(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if answer.question.can_vote(request):
        Vote.objects.create(answer=answer)
        answer.question.set_voted(request)
    return HttpResponseRedirect(request.GET.get('back', request.META.get('HTTP_REFERER', '/')))

