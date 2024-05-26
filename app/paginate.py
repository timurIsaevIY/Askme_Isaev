from django.core.paginator import Paginator

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    count = paginator.num_pages
    try:
        page_num = int(request.GET.get('page', 1))
        if page_num <= 0:
            page_num = 1
        elif page_num > count:
            page_num = count
    except:
        page_num = 1
    page_obj = paginator.page(page_num)
    paginator_elements = [i for i in range(max(page_num - 4, 1), min(page_num + 4, count) + 1)]
    return [page_obj, page_num, count, paginator_elements]