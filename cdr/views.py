from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .forms import AsteriskForm, DateTimeForm, DurationTimeForm
from .models import Asterisk
import datetime
import calendar


@login_required
def home(request):
    if request.method == 'GET':

        rows = 10
        page = 1
        cdr_form = AsteriskForm(request.GET or None, initial={'rows': rows})
        if cdr_form.is_valid():
            rows = cdr_form.cleaned_data.get('rows', rows) or rows
            page = cdr_form.cleaned_data.get('page', page) or page
            print('cdr_form.cleaned_data: %s' % cdr_form.cleaned_data)
            print('cdr_form.duration_start:%s' % cdr_form.duration_start)
            print('cdr_form.duration_end:%s' % cdr_form.duration_end)
            print('cdr_form.datetime_start:%s' % cdr_form.datetime_start)
            print('cdr_form.datetime_end:%s' % cdr_form.datetime_end)

        calls_list = Asterisk.objects.all()

        paginator = Paginator(calls_list, rows)  # Show 'count' calls per page
        try:
            calls = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            calls = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            calls = paginator.page(paginator.num_pages)

        date = datetime.datetime.now()
        return render(request, 'cdr/home.html', {
            'yesterday': date - datetime.timedelta(days=1),
            'week_ago': date - datetime.timedelta(days=7),
            '2week_ago': date - datetime.timedelta(days=14),
            'this_month': datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month)[1]),
            'last_month': datetime.date(date.year, date.month-1, calendar.monthrange(date.year, date.month-1)[1]),
            'cdr_form': cdr_form,
            'calls': calls,
        })

    return HttpResponseForbidden()
