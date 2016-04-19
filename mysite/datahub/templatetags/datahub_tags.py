from django import template
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import format_html_join

from ..models import Tag


register = template.Library()


@register.simple_tag(takes_context=True)##notice the takes_context=True to be able to retrieve a context (for the template at the end)
def tagcloud(context, owner=None):
    url = reverse('datahub:document_list')
    filters = {'document__is_public': True}

    if owner is not None:
        url = reverse('datahub:document_user',
            kwargs={'username': owner.username})
        filters['document__owner'] = owner
    if context['user'] == owner:
        del filters['document__is_public']
	#database query start
    tags = Tag.objects.filter(**filters)
    tags = tags.annotate(count=models.Count('document'))##anotate the tag with the number of documents under that tag
    tags = tags.order_by('name').values_list('name', 'count')## order orders and values_list convert the query set to a list of tuples
    fmt = '<a href="%s?tag={0}">{0} ({1})</a>' % url ##a string to render the actual HTML of the tag
    return format_html_join(', ', fmt, tags)##HTML for all tags comma separeted
