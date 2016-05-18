from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Asterisk


@login_required
def home(request):
    calls_list = Asterisk.objects.all()

    count = request.GET.get('count', default=10)
    page = request.GET.get('page', default=1)

    paginator = Paginator(calls_list, count)  # Show 10 calls per page
    try:
        calls = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        calls = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        calls = paginator.page(paginator.num_pages)

    return render(request, 'cdr/home.html', {'calls': calls})
