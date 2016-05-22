from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .forms import AsteriskForm
from .models import Asterisk


@login_required
def home(request):
    if request.method == 'GET':
        calls_list = Asterisk.objects.all()

        rows = request.GET.get('rows')
        if not rows or rows is None:
            rows = 10

        page = request.GET.get('page')
        if not page or page is None:
            page = 1

        # TODO: move this to settings.py
        call_states_list = ('CALL_REJECTED', 'INVALID_NUMBER_FORMAT', 'USER_BUSY', 'NORMAL_CLEARING', 'NO_ANSWER',)
        call_states = list()
        for state in call_states_list:
            call_states.append((state, True if 'call_state-%s' % state in request.GET else False,))

        call_filters_list = (('src-number', 'Src Number',),
                             ('dst-number', 'Dst Number',),
                             ('dispatcher-number', 'Dispatcher Number',),)
        call_filters = list()
        call_filters_data = dict()
        for name, label in call_filters_list:
            option = 'start'
            if '%s-option' % name in request.GET:
                c = request.GET.get('%s-option' % name)
                if c == 'end' or c == 'start' or c == 'equal' or c == 'contains':
                    option = c
            value = ''
            if name in request.GET:
                value = request.GET.get(name)  # TODO: filter for DID number
                call_filters_data[name] = value
            call_filters.append((name, value, label, option, True if '%s-not' % name in request.GET else False,))

        paginator = Paginator(calls_list, rows)  # Show 'count' calls per page
        try:
            calls = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            calls = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            calls = paginator.page(paginator.num_pages)

        cdr_form = AsteriskForm(request.GET or None)

        return render(request, 'cdr/home.html', {
            'call_filters': call_filters,
            'call_states': call_states,
            'cdr_form': cdr_form,
            'calls': calls,
            'rows': rows
        })

    return HttpResponseForbidden()
