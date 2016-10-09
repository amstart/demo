from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.utils import timezone
from switch import Switch

from demoslogic.users.models import User
from .models import Choice, Premise
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm


class NewPremiseView(TemplateView):
    template_name = 'premises/new_premise.html'

class PremiseCreateView(CreateView):
    template_name = 'premises/create_premise.html'
    success_url = '/'
    model = Premise

    def get_form_class(self):
        with Switch(self.kwargs['mode']) as case:
            if case('SubjectPredicate'):
                return SubjectPredicateInputForm
            if case('WithComplementedObject'):
                return WithComplementedObjectInputForm
            if case('WithObject'):
                return WithObjectInputForm
            if case('WithComplement'):
                return WithComplementInputForm

    def get(self, request, *args, **kwargs):
        try:
            response = super(PremiseCreateView, self).get(request, *args, **kwargs)
        except:
            raise Http404('Page does not exist.')
        return response

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        super(PremiseCreateView, self).form_valid(form)
        return HttpResponseRedirect(reverse('premises:index') + '%d/' % (self.object.pk,))

class PremisesListView(ListView):
    template_name = 'premises/index.html'
    context_object_name = 'premise_list'
    model = Premise
    # def get_queryset(self):
    #     return Premise.objects.all().order_by('-subject')

class UnstagedPremisesListView(ListView):
    template_name = 'premises/index_unstaged.html'
    context_object_name = 'premise_list'

    def get_queryset(self):
        return Premise.objects.exclude(staged__isnull=False).order_by('-pub_date')[:]


class PremiseDetailView(DetailView):
    model = Premise
    template_name = 'premises/detail.html'

class DeletePremiseView(DeleteView):
    model = Premise
    success_url = reverse_lazy('premises:index')

class PremiseVotesView(DetailView):
    model = Premise
    template_name = 'premises/results.html'


def vote(request, premise_id):
    premise = get_object_or_404(Premise, pk = premise_id)
    try:
        selected_choice = premise.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the premise voting form.
        return render(request, 'premises/detail.html', {
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
