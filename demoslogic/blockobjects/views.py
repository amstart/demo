# -*- coding: utf-8 -*-
import sys
from allauth.account.decorators import login_required

from django import http
from django.views.debug import ExceptionReporter
from django.contrib.auth import login
from django.views.debug import ExceptionReporter
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.users.models import User

class DetailWithVoteView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(DetailWithVoteView, self).get_context_data(**kwargs)
        context['voteform'] = self.voteform
        context['already_voted'] = 0
        return context

    def render_to_response(self, context, **kwargs):
        if self.request.user.is_authenticated:
            voteobjects = self.voteform.Meta.model.objects.filter(user = self.request.user).filter(object = self.object)
            if voteobjects.count():
                del context['voteform']
                context['already_voted'] = voteobjects[0].value
                if voteobjects.count() > 1:
                    raise Exception('More than one vote object found!')
            else:
                self.voteform.fields['value'].initial = None #this seems to be required for an unkown reason
        return super(DetailWithVoteView, self).render_to_response(context, **kwargs)

    @method_decorator(login_required)
    def post(self, request, **post_data):
        voteform = type(self.voteform)(request.POST)
        pk = post_data['pk']
        if voteform.is_valid():
            # if self.request.user.is_authenticated:
            votemodel = self.voteform.Meta.model
            voteobjects = votemodel.objects.filter(user = self.request.user).filter(object_id = pk)
            if voteobjects.count():
                raise Exception('There is already a vote!!')
            vote = votemodel(object_id = pk, user = request.user)
            vote.update(voteform.cleaned_data['value'])
            return HttpResponseRedirect(request.get_full_path())
        else:
            return render(request, self.template_name,
                          {'premise': Premise.objects.get(pk = pk), 'voteform': voteform})


class UpdateVoteView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(UpdateVoteView, self).get_context_data(**kwargs)
        context['voteform'] = self.voteform
        return context

    def render_to_response(self, context, **kwargs):
        votemodel = self.voteform.Meta.model
        voteobjects = votemodel.objects.filter(user = self.request.user).filter(object = self.object)
        self.voteform.fields['value'].initial = voteobjects[0].value
        if voteobjects.count() > 1:
            raise Exception('More than one vote object found!')
        return super(UpdateVoteView, self).render_to_response(context, **kwargs)

    def post(self, request, **post_data):
        voteform = type(self.voteform)(request.POST)
        pk = post_data['pk']
        if voteform.is_valid():
            votemodel = self.voteform.Meta.model
            voteobjects = votemodel.objects.filter(user = self.request.user).filter(object_id = pk)
            if voteobjects.count() > 1:
                raise Exception('More than one vote object found!')
            vote = voteobjects[0]
            vote.update(voteform.cleaned_data['value'])
            return HttpResponseRedirect(reverse('premises:detail', args = [pk]))
        else:
            return render(request, self.template_name,
                          {self.model.__name__: self.model.objects.get(pk = pk),
                           'voteform': voteform})

def show_server_error(request):
    """
    500 error handler to show Django default 500 template
    with nice error information and traceback.
    Useful in testing, if you can't set DEBUG=True.

    Templates: `500.html`
    Context: sys.exc_info() results
     """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error = ExceptionReporter(request, exc_type, exc_value, exc_traceback)
    return http.HttpResponseServerError(error.get_traceback_html())

def LoginSeleniumView(request):
    users = User.objects.all()
    login(request, users[0])
    return http.HttpResponseRedirect(reverse('users:detail', kwargs={'username': users[0].username}))
