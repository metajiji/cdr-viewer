from django.template import Library
from django.core.urlresolvers import reverse, resolve, NoReverseMatch

register = Library()


@register.simple_tag
def nav_active(request_uri, uris, data='active', **kwargs):
    """
    Description:
        Highlight bootstrap nav menu by 'active'.
    Usage:
        For url patterns:
            url(r'^accounts/add/(?P<server_id>\d+)/$', views.accounts_add, {}, name='accounts_add'),
            url(r'^accounts/manage/(?P<server_id>\d+)/$', views.accounts_manage, {}, name='accounts_manage'),
        Use code in template:
            <li class="foo {% nav_active request.path 'cp:manage cp:add' 'current' server_id=server.id %}">foo bar</li>
            Or highlight with any server_id value:
            <li{% nav_active request.path 'cp:manage' ' class="active"' %}>foo bar</li>

        For url pattern:
            url(r'^accounts/edit/(?P<server_id>\d+)/(?P<account_id>\d+)/$',
                views.accounts_edit, {}, name='accounts_edit'),
        Use code in template:
            <li class="foo bar {% nav_active request.path 'cp:manage' %}">foo bar</li>

        For url pattern:
            url(r'^$', views.home, name='home'),
        Use code in template:
            <li{% nav_active request.path 'cp:home' ' class="active"' %}>foo bar</li>
    """

    for uri in uris.split():
        match = resolve(request_uri)
        try:
            if reverse(uri, kwargs=match.kwargs) == request_uri:
                for key in kwargs:
                    if key in match.kwargs:
                        if str(kwargs[key]) != str(match.kwargs[key]):
                            return ''
                return data
        except NoReverseMatch:
            pass
    return ''
