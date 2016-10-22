# -*- coding: utf-8 -*-
import sys
from django import http
from django.views.debug import ExceptionReporter

from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.views.debug import ExceptionReporter
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

from .users.models import User

class DetailWithVoteView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(DetailWithVoteView, self).get_context_data(**kwargs)
        context['vote_maxvalue'] = 4 #self.viewobject.max_value
        context['voteform'] = self.voteform
        return context

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
