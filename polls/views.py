from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Premise


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_premise_list'

    def get_queryset(self):
        """
        Return the last five published premises (not including those set to be
        published in the future).
        """
        return Premise.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def post(self, request, *args, **kwargs):
        return add_item(request)

def add_item(request):
    new_premise = Premise(subject=request.POST.get('item_text', 'unnamed'), pub_date=timezone.now())
    new_premise.save()
    return HttpResponseRedirect(reverse('premises:index'))


class DetailView(generic.DetailView):
    model = Premise
    template_name = 'polls/detail.html'
    def post(self, request, *args, **kwargs):
        return remove_item(request)

def remove_item(request):
    print(request.POST['delete_premise'])
    premise = get_object_or_404(Premise, pk=request.POST['delete_premise'])
    premise.delete()
    return HttpResponseRedirect(reverse('premises:index'))


class ResultsView(generic.DetailView):
    model = Premise
    template_name = 'polls/results.html'

def vote(request, premise_id):
    premise = get_object_or_404(Premise, pk=premise_id)
    try:
        selected_choice = premise.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the premise voting form.
        return render(request, 'polls/detail.html', {
            'premise': premise,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('premises:results', args=(premise.id,)))
