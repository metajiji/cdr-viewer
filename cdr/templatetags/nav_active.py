from django.template import Library
from django.core.urlresolvers import reverse, resolve, NoReverseMatch


register = Library()


@register.simple_tag
def nav_active(request_uri, uris, data='class="active"', **kwargs):
    """
    Description:
        Highlight bootstrap nav menu by 'class="active"'.
    Usage:
        For urlpatterns:
            url(r'^accounts/add/(?P<server_id>\d+)/$', views.accounts_add, {}, name='accounts_add'),
            url(r'^accounts/manage/(?P<server_id>\d+)/$', views.accounts_manage, {}, name='accounts_manage'),
        Use code in template:
            {% nav_active request.path 'cp:accounts_manage cp:accounts_add' 'active' server_id=server.server_id.id %}
            Or highlight with any server_id value:
            {% nav_active request.path 'cp:accounts_manage' 'active' %}

        For urlpattern:
            url(r'^accounts/edit/(?P<server_id>\d+)/(?P<account_id>\d+)/$',
                views.accounts_edit, {}, name='accounts_edit'),
        Use code in template:
            url(r'^accounts/conf/(?P<server_id>\d+)/(?P<account_id>\d+)/$',
                views.accounts_conf, {}, name='accounts_conf'),

        For urlpattern:
            url(r'^$', views.home, name='home'),
        Use code in template:
            {% nav_active request.path 'cp:home' %}
    """

    for uri in uris.split():
        match = resolve(request_uri)
        try:
            if reverse(uri, kwargs=match.kwargs) == request_uri:
                for key, value in kwargs.iteritems():
                    if key in match.kwargs:
                        if str(value) != str(match.kwargs[key]):
                            return ''
                return data
        except NoReverseMatch:
            pass  # return ''
    return ''
