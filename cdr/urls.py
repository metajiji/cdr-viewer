"""cdr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
# from .views import cdr
from . import views

# TODO x-accel-redirect.
# https://toster.ru/q/208755
urlpatterns = [
    # Auth
    url('^login/$', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    url('^logout/$', auth_views.logout, {'template_name': 'auth/logout.html'}, name='logout'),
    url('^password_change/$', auth_views.password_change, {'template_name': 'auth/password_change.html'},
        name='password_change'),
    url('^password_change_done/$', auth_views.password_change_done, name='password_change_done'),

    # Admin
    url(r'^admin/', admin.site.urls),

    # Application
    url(r'^$', RedirectView.as_view(pattern_name='home')),
    url(r'^cdr/', views.home, name='home'),
]

# TODO: development serve static and media files
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
