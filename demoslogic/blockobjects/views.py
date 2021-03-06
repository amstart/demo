# -*- coding: utf-8 -*-
import sys
from allauth.account.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django import http
from django.views.debug import ExceptionReporter
from django.contrib.auth import login
from django.views.debug import ExceptionReporter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.users.models import User
from demoslogic.premises import models
from demoslogic.arguments.models import Argument

def clean_view(request):
    qset = models.Noun.objects.all()
    for obj in qset:
        obj_set = obj.key_subject.all() | obj.key_object.all() | obj.key_indirect_object.all()
        if not obj_set.count():
            obj.delete()
    qset = models.Adjective.objects.all()
    for obj in qset:
        obj_set = obj.premise_set.all()
        if not obj_set.count():
            obj.delete()
    qset = models.Premise.objects.all()
    for obj in qset:
        obj_set = obj.premise1.all() | obj.premise2.all() | obj.premise3.all() | obj.conclusion.all()
        if not obj_set.count():
            obj.delete()
        obj.save()
    return HttpResponseRedirect(reverse('home'))

class NetworkView(TemplateView):
    template_name = 'blockobjects/network.html'

    def get_context_data(self, **kwargs):
        return self.compute_network()

    @staticmethod
    def compute_network():
        arguments_qs = Argument.objects.values('id', 'premise1', 'premise2', 'premise3', 'conclusion',
                                               'aim', 'premise1_if', 'premise2_if', 'premise3_if', 'sentence')
        arguments = [entry for entry in arguments_qs]
        statements_qs = models.Premise.objects.values('id', 'premise_type', 'sentence')
        nodes = [entry for entry in statements_qs]
        for node in nodes:
            node['group'] = 1
            node['id'] = 'p' + str(node['id'])
            node['name'] = node.pop('sentence')
        links = []
        for argument in arguments:
            node_id = 'a' + str(argument['id'])
            arg_sentence = argument['sentence']
            nodes.append({'id': node_id, 'group': 2, 'name': arg_sentence})
            links.append({'source': 'p' + str(argument['premise1']), 'target': node_id,
                          'value': 2, 'aim': argument['premise1_if']})
            if argument['premise2']:
                links.append({'source': 'p' + str(argument['premise2']), 'target': node_id,
                              'value': 2, 'aim': argument['premise2_if']})
            if argument['premise3']:
                links.append({'source': 'p' + str(argument['premise3']), 'target': node_id,
                              'value': 2, 'aim': argument['premise3_if']})
            links.append({'source': node_id, 'target': 'p' + str(argument['conclusion']),
                          'value': 1, 'aim': argument['aim']})
        return {'nodes': nodes, 'links': links}

class ObjectListView(ListView):
    template_name = 'blockobjects/index.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(ObjectListView, self).get_context_data(**kwargs)
        context['model_name'] = self.model.name_upper
        context['model_namespace'] = self.model.namespace
        if self.request.path.find("unstaged")  == -1:
            context['heading'] = self.model.name_upper + "s"
        else:
            context['heading'] = "Unstaged " + self.model.name_upper + "s"
        return context

    def get_queryset(self):
        if self.request.path.find("unstaged")  == -1:
            return self.model.objects.all()
        else:
            return self.model.objects.exclude(staged__isnull=False)


class CreateObjectView(LoginRequiredMixin, CreateView):
    def form_valid(self, form): #login_required somwhere?
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(reverse(self.object.namespace + ':detail', args = [self.object.pk]))

    def get_context_data(self, **kwargs):
        context = super(CreateObjectView, self).get_context_data(**kwargs)
        context['model_namespace'] = self.model.namespace
        context['model_name_upper'] = self.model.name_upper
        context['model_name_lower'] = self.model.name_lower
        return context

class DeleteObjectView(LoginRequiredMixin, DeleteView):
    template_name = 'blockobjects/delete_object.html'

class DetailWithVoteView(DetailView):
    template_name = 'blockobjects/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailWithVoteView, self).get_context_data(**kwargs)
        context['user_choice'] = 0
        context['already_voted'] = 0
        return context

    def plot(self, context, voteobject_user, voteobjects_all):
        plot_data = voteobject_user.get_plot_data(voteobjects_all, 'value')
        context['plot_data'] = plot_data
        if hasattr(self.voteform.Meta.model, 'value2'):
            plot_data2 = voteobject_user.get_plot_data(voteobjects_all, 'value2')
            context['plot_data2'] = plot_data2
        return context

    def render_to_response(self, context, **kwargs):
        voteform = self.voteform(object = self.object)
        context['voteform'] = voteform
        if self.request.user.is_authenticated:
            votemodel = voteform.Meta.model
            voteobjects_all = votemodel.objects.filter(object = self.object)
            voteobjects_user = voteobjects_all.filter(user = self.request.user)
            if voteobjects_user.count():
                del context['voteform']
                context['user_choice'] = voteobjects_user[0].value
                context['already_voted'] = 1
                if voteobjects_user.count() > 1:
                    raise Exception('More than one vote object found!')
                context = self.plot(context, voteobjects_user[0], voteobjects_all)
            else:
                voteform.fields['value'].initial = None #this seems to be required for an unkown reason
        return super(DetailWithVoteView, self).render_to_response(context, **kwargs)

    @method_decorator(login_required)
    def post(self, request, **post_data):
        voteform = self.voteform(request.POST)
        pk = post_data['pk']
        if voteform.is_valid():
            # if self.request.user.is_authenticated:
            votemodel = self.voteform.Meta.model
            voteobjects = votemodel.objects.filter(user = self.request.user).filter(object_id = pk)
            if voteobjects.count():
                raise Exception('There is already a vote!!')
            vote = votemodel(object_id = pk, user = request.user)
            vote.update(voteform.cleaned_data['value'], voteform.cleaned_data.get('value2', None))
            return HttpResponseRedirect(request.get_full_path())
        else:
            return render(request, self.template_name,
                          {'premise': votemodel.obj_mdl.objects.get(pk = pk), 'voteform': voteform})


class UpdateVoteView(LoginRequiredMixin, DetailView):
    template_name = 'blockobjects/update_vote.html'

    def render_to_response(self, context, **kwargs):
        voteform = self.voteform(object = self.object)
        context['voteform'] = voteform
        votemodel = voteform.Meta.model
        voteobjects = votemodel.objects.filter(user = self.request.user).filter(object = self.object)
        voteform.fields['value'].initial = voteobjects[0].value
        if voteobjects.count() > 1:
            raise Exception('More than one vote object found!')
        return super(UpdateVoteView, self).render_to_response(context, **kwargs)

    def post(self, request, **post_data):
        voteform = self.voteform(request.POST)
        pk = post_data['pk']
        if voteform.is_valid():
            votemodel = self.voteform.Meta.model
            voteobjects = votemodel.objects.filter(user = self.request.user).filter(object_id = pk)
            if voteobjects.count() > 1:
                raise Exception('More than one vote object found!')
            vote = voteobjects[0]
            vote.update(voteform.cleaned_data['value'], voteform.cleaned_data.get('value2', None))
            return HttpResponseRedirect(reverse(votemodel.obj_mdl.namespace + ':detail', args = [pk]))
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
    return http.HttpResponse('errpr')
    # return http.HttpResponseServerError(error.get_traceback_html())

def LoginSeleniumView(request):
    users = User.objects.all()
    login(request, users[0])
    return http.HttpResponseRedirect(reverse('users:detail', kwargs={'username': users[0].username}))
