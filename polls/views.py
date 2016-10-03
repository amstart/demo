from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from django import forms
from switch import Switch

from .models import Choice, Premise

class PremiseFullInputForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object', 'complement']

class PremiseWithObjectInputForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object']

class PremiseMinimumInputForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'complement']

class PremiseCreateView(CreateView):
    template_name = 'polls/new_premise.html'
    success_url = '/'
    model = Premise

    def get_form_class(self):
        with Switch(self.kwargs['mode']) as case:
            if case('full'):
                return PremiseFullInputForm
            if case('obj'):
                return PremiseWithObjectInputForm
            if case('min'):
                return PremiseMinimumInputForm

    def form_valid(self, form):
        self.object = form.save()
        super(PremiseCreateView, self).form_valid(form)
        return HttpResponseRedirect(reverse('premises:index') + '%d/' % (self.object.pk,))

class PremisesListView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'premise_list'
    model = Premise
    # def get_queryset(self):
    #     return Premise.objects.all().order_by('-subject')

class UnstagedPremisesListView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'premise_list'

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


class PremiseDetailView(DetailView):
    model = Premise
    template_name = 'polls/detail.html'

    def post(self, request, *args, **kwargs):
        return remove_item(request)


class PremiseVotesView(DetailView):
    model = Premise
    template_name = 'polls/results.html'


def add_item(request):
    new_premise = Premise(subject=request.POST.get('item_text', 'unnamed'), pub_date=timezone.now())
    new_premise.save()
    return HttpResponseRedirect(reverse('premises:index') + '%d/' % (new_premise.pk,))

def remove_item(request):
    print(request.POST['delete_premise'])
    premise = get_object_or_404(Premise, pk=request.POST['delete_premise'])
    premise.delete()
    return HttpResponseRedirect(reverse('premises:index'))

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
