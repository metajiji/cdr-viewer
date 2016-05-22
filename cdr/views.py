from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .forms import AsteriskForm, DateTimeForm, DurationTimeForm
from .models import Asterisk


@login_required
def home(request):
    if request.method == 'GET':

        # TODO: Validate here fields 'datetime' and 'duration' manually
        data = dict()
        datetime = request.GET.get('datetime', None)
        if datetime is not None:
            datetime = datetime.split()
            if len(datetime) == 5:  # field format: 'YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss'
                data['start'] = '%s %s' % (datetime[0], datetime[1])
                data['end'] = '%s %s' % (datetime[3], datetime[4])
                datetime_form = DateTimeForm(data=data)
                if datetime_form.is_valid():
                    print('datetime_form.cleaned_data.start: %s' % datetime_form.cleaned_data.get('start'))
                    print('datetime_form.cleaned_data.end: %s' % datetime_form.cleaned_data.get('end'))
            else:
                # TODO: add_error to cdr_form.datetime
                print('datetime field must be format "YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss"')

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
                print('duration field must be format "HH:mm:ss - HH:mm:ss"')

        cdr_form = AsteriskForm(request.GET)
        if cdr_form.is_valid():
            print('cdr_form.cleaned_data: %s' % cdr_form.cleaned_data)

        calls_list = Asterisk.objects.all()
        rows = request.GET.get('rows')
        if not rows or rows is None:
            rows = 10

        page = request.GET.get('page')
        if not page or page is None:
            page = 1

        paginator = Paginator(calls_list, rows)  # Show 'count' calls per page
        try:
            calls = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            calls = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            calls = paginator.page(paginator.num_pages)

        return render(request, 'cdr/home.html', {
            # 'call_filters': call_filters,
            # 'call_states': call_states,
            'cdr_form': cdr_form,
            'calls': calls,
            # 'rows': rows
        })

    return HttpResponseForbidden()
