from switch import Switch

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.utils import timezone
from allauth.account.decorators import login_required
from django.utils.decorators import method_decorator

from demoslogic.users.models import User
from demoslogic.blockobjects.views import DetailWithVoteView

from .models import Premise, CategorizationVote
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class PremiseDetailView(DetailWithVoteView):
    model = Premise
    template_name = 'premises/detail.html'
    voteform = CategorizationVoteForm()

    def render_to_response(self, context, **kwargs):
        if self.request.user.is_authenticated:
            voteobjects = self.voteform.Meta.model.objects.filter(user = self.request.user).filter(object = self.object)
            if voteobjects.count():
                self.voteform.fields['value'].initial = voteobjects[0].value
                context['already_voted'] = True
                if voteobjects.count() > 1:
                    raise Exception('More than one vote object found!')
            else:
                self.voteform.fields['value'].initial = None #this seems to be required for an unkown reason
        return super(PremiseDetailView, self).render_to_response(context, **kwargs)

    @method_decorator(login_required)
    def post(self, request, **post_data):
        voteform = CategorizationVoteForm(request.POST)
        pk = post_data['pk']
        if voteform.is_valid():
            # if self.request.user.is_authenticated:
            voteobjects = self.voteform.Meta.model.objects.filter(
                user = self.request.user).filter(object_id = pk)
            if voteobjects.count():
                vote = voteobjects[0]
                if voteobjects.count() > 1:
                    raise Exception('More than one vote object found!')
            else:
                vote = CategorizationVote(object_id = pk,
                                          value = 1,
                                          user = request.user)
            vote.update(voteform.cleaned_data['value'])
            return HttpResponseRedirect(request.get_full_path())
        else:
            return render(request, self.template_name,
                          {'premise': Premise.objects.get(pk = pk), 'voteform': voteform})

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
