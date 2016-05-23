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

        data = dict()
        date_time = request.GET.get('datetime', None)
        if date_time is not None:
            date_time = date_time.split()
            if len(date_time) == 5:  # field format: 'YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss'
                data['start'] = '%s %s' % (date_time[0], date_time[1])
                data['end'] = '%s %s' % (date_time[3], date_time[4])
                datetime_form = DateTimeForm(data=data)
                if datetime_form.is_valid():
                    print('datetime_form.cleaned_data.start: %s' % datetime_form.cleaned_data.get('start'))
                    print('datetime_form.cleaned_data.end: %s' % datetime_form.cleaned_data.get('end'))
                else:
                    # TODO: add_error to cdr_form.datetime
                    print('datetime field must be format "YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss"')
            else:
                # TODO: add_error to cdr_form.datetime
                print('datetime field is invalid, this field must be format "YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss"')

        duration = request.GET.get('duration', None)
        if duration is not None:
            duration = duration.split()
            if len(duration) == 3:  # field format: 'HH:mm:ss - HH:mm:ss'
                data['start'] = duration[0]
                data['end'] = duration[2]
                duration_form = DurationTimeForm(data=data)
                if duration_form.is_valid():
                    print('duration_form.cleaned_data.start: %s' % duration_form.cleaned_data.get('start'))
                    print('duration_form.cleaned_data.end: %s' % duration_form.cleaned_data.get('end'))
                else:
                    # TODO: add_error to cdr_form.duration
                    print('duration field is invalid, this field must be format "HH:mm:ss - HH:mm:ss"')
            else:
                # TODO: add_error to cdr_form.duration
                print('duration field must be format "HH:mm:ss - HH:mm:ss"')

        rows = 10
        page = 1
        cdr_form = AsteriskForm(request.GET or None, initial={'rows': rows})
        if cdr_form.is_valid():
            rows = cdr_form.cleaned_data.get('rows', rows) or rows
            page = cdr_form.cleaned_data.get('page', page) or page
            print('cdr_form.cleaned_data: %s' % cdr_form.cleaned_data)

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
