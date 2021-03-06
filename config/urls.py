# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from demoslogic.blockobjects import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^blogs/$', TemplateView.as_view(template_name='pages/blogs.html'), name='blogs'),
    url(r'^help/$', TemplateView.as_view(template_name='pages/help.html'), name='help'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('demoslogic.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    #DEBUG
    url(
        regex=r'^selenium/$',
        view=views.LoginSeleniumView,
        name='selenium'
    ),
    # Your stuff: custom urls includes go here
    url(r'^visualize/', views.NetworkView.as_view(), name='network'),
    url(r'^clean', views.clean_view, name='clean'),
    url(r'^qstatements/', include('demoslogic.premises.urls')),
    url(r'^arguments/', include('demoslogic.arguments.urls')),
    url(r'^evidences/', include('demoslogic.evidences.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.TESTING_MODE:
    # enable this handler only for testing,
    # so that if DEBUG=False and we're not testing,
    # the default handler is used
    handler500 = 'demoslogic.blockobjects.views.show_server_error'

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
