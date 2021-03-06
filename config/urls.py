"""Unicorn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^adminBostoncocoon/', admin.site.urls),
    url(r'^', include('cocoon.homePage.urls')),
    url(r'^userAuth/', include('cocoon.userAuth.urls')),
    url(r'^houseDatabase/', include('cocoon.houseDatabase.urls')),
    url(r'^commutes/', include('cocoon.commutes.urls')),
    url(r'^survey/', include('cocoon.survey.urls')),
    url(r'^scheduler/', include('cocoon.scheduler.urls')),
    url(r'^signatures/', include('cocoon.signature.urls')),
    url(r'^password_reset/$', auth_views.password_reset,
        {
            'post_reset_redirect': reverse_lazy('password_reset_done'),
            'html_email_template_name': 'registration/password_reset_html_email.html'
        },
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'cocoon.views.error_404_view'
