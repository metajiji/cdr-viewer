from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .forms import AsteriskForm
from .models import Asterisk
import datetime
import calendar


@login_required
def home(request):
    if request.method == 'GET':
        calls_list = Asterisk.objects.all()

        rows = 10
        page = 1
        cdr_form = AsteriskForm(request.GET or None, initial={'rows': rows})
        if cdr_form.is_valid():
            rows = cdr_form.cleaned_data.get('rows', rows) or rows
            page = cdr_form.cleaned_data.get('page', page) or page

            if cdr_form.cleaned_data['src_number'] != '':
                if cdr_form.cleaned_data['src_number_option'] == 'start':
                    if 'src_number_not' in request.GET:
                        calls_list = calls_list.exclude(src__istartswith=cdr_form.cleaned_data['src_number'])
                    else:
                        calls_list = calls_list.filter(src__istartswith=cdr_form.cleaned_data['src_number'])
                elif cdr_form.cleaned_data['src_number_option'] == 'end':
                    if 'src_number_not' in request.GET:
                        calls_list = calls_list.exclude(src__iendswith=cdr_form.cleaned_data['src_number'])
                    else:
                        calls_list = calls_list.filter(src__iendswith=cdr_form.cleaned_data['src_number'])
                elif cdr_form.cleaned_data['src_number_option'] == 'equal':
                    if 'src_number_not' in request.GET:
                        calls_list = calls_list.exclude(src__iexact=cdr_form.cleaned_data['src_number'])
                    else:
                        calls_list = calls_list.filter(src__iexact=cdr_form.cleaned_data['src_number'])
                elif cdr_form.cleaned_data['src_number_option'] == 'contains':
                    if 'src_number_not' in request.GET:
                        calls_list = calls_list.exclude(src__icontains=cdr_form.cleaned_data['src_number'])
                    else:
                        calls_list = calls_list.filter(src__icontains=cdr_form.cleaned_data['src_number'])

            if cdr_form.cleaned_data['dst_number'] != '':
                if cdr_form.cleaned_data['dst_number_option'] == 'start':
                    if 'dst_number_not' in request.GET:
                        calls_list = calls_list.exclude(dst__istartswith=cdr_form.cleaned_data['dst_number'])
                    else:
                        calls_list = calls_list.filter(dst__istartswith=cdr_form.cleaned_data['dst_number'])
                elif cdr_form.cleaned_data['dst_number_option'] == 'end':
                    if 'dst_number_not' in request.GET:
                        calls_list = calls_list.exclude(dst__iendswith=cdr_form.cleaned_data['dst_number'])
                    else:
                        calls_list = calls_list.filter(dst__iendswith=cdr_form.cleaned_data['dst_number'])
                elif cdr_form.cleaned_data['dst_number_option'] == 'equal':
                    if 'dst_number_not' in request.GET:
                        calls_list = calls_list.exclude(dst__iexact=cdr_form.cleaned_data['dst_number'])
                    else:
                        calls_list = calls_list.filter(dst__iexact=cdr_form.cleaned_data['dst_number'])
                elif cdr_form.cleaned_data['dst_number_option'] == 'contains':
                    if 'dst_number_not' in request.GET:
                        calls_list = calls_list.exclude(dst__icontains=cdr_form.cleaned_data['dst_number'])
                    else:
                        calls_list = calls_list.filter(dst__icontains=cdr_form.cleaned_data['dst_number'])

            # TODO: dispatcher_number
            # if cdr_form.cleaned_data['dispatcher_number'] != '':
            #     if cdr_form.cleaned_data['dispatcher_number_option'] == 'start':
            #         if 'dispatcher_number_not' in request.GET:

            # calls_list = calls_list.filter(calldate__gte=cdr_form.datetime_start, calldate__lte=cdr_form.datetime_end)
            calls_list = calls_list.filter(calldate__range=(cdr_form.datetime_start, cdr_form.datetime_end))

            # TODO: duration
            # calls_list = calls_list.filter(duration__range=(cdr_form.duration_start, cdr_form.duration_end))

            if len(cdr_form.cleaned_data['call_state']) > 0:
                calls_list = calls_list.filter(disposition__in=cdr_form.cleaned_data['call_state'])

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
