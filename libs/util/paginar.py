from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def listing(request, queryset, num=10):
    if queryset is None:
        return []
    elif queryset.count() == 0:
        return []
    paginator = Paginator(queryset, num)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pages = paginator.page(paginator.num_pages)
    return pages
