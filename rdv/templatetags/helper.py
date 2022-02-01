from django import template
from urllib.parse import urlencode
from collections import OrderedDict

register = template.Library()

@register.inclusion_tag('tags/sort_link.html')
def paginator_sort(request, field, content):
    params = request.GET.copy()
    key = 'sort'
    cls = ''

    if key in params.keys():
        if params[key].startswith('-') and params[key].lstrip('-') == field:
            params[key] = field
            cls = 'desc'
        elif params[key].lstrip('-') == field:
            params[key] = '-' + field
            cls = 'asc'
        else:
            params[key] = field
    else:
        params[key] = field

    url = '?' + urlencode(OrderedDict(sorted(params.items())))

    return {'url': url, 'cls': cls, 'content': content}
