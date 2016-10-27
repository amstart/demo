from switch import Switch
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.utils import timezone

from demoslogic.users.models import User
from demoslogic.blockobjects.views import DetailWithVoteView, UpdateVoteView

from .models import Premise, CategorizationVote
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class PremiseDetailView(DetailWithVoteView):
    model = Premise
    template_name = 'premises/detail.html'
    voteform = CategorizationVoteForm()

class PremiseUpdateView(UpdateVoteView):
    model = Premise
    template_name = 'premises/update.html'
    voteform = CategorizationVoteForm()


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

    def form_valid(self, form): #login_required somwhere?
        form.instance.user = self.request.user
        self.object = form.save()
        super(PremiseCreateView, self).form_valid(form)
        print(self.object.pk)
        return HttpResponseRedirect(reverse('premises:detail', args = [self.object.pk]))

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


class DeletePremiseView(DeleteView):
    model = Premise
    success_url = reverse_lazy('premises:index')

class PremiseVotesView(DetailView):
    model = Premise
    template_name = 'premises/results.html'
