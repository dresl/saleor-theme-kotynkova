import json

from django.template import Library
from django.utils.http import urlencode
from saleor.product.models import Collection, Category
from django.conf import settings
from django.utils.safestring import SafeString
from fullcalendar.models import CalendarEvent

register = Library()

@register.inclusion_tag('product/product_collection.html')
def collection_prodcuts(collection_slug, template_style, count=None):
    collection = Collection.objects.get(slug=collection_slug)
    return {
        'product_list': collection.products.all().order_by('-updated_at')[:count],
        'template_style': template_style,
        }

@register.filter(name='count_products')
def count_products(value):
    counted = 0
    for product, availability in value:
        if product:
            counted += 1
    return counted

@register.simple_tag
def fullcalendar_config():
    events = CalendarEvent.objects.all()
    final_config = SafeString("""{  timeFormat: "H:mm",
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: '',
                },
                allDaySlot: false,
                locale: 'cs',
                firstDay: 1,
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 8,
                maxTime: 20,
                editable: false,
                eventClick: function(event, jsEvent, view) {
                    
                },
                events: [
            """)
    for event in events:
        final_config += SafeString("{" + "title:" + "'{}'".format(event.title) + ",")
        final_config += SafeString("start:" + "'{}-{}T{}'".format(event.start.year, event.start.strftime("%m-%d"), event.start.strftime("%H:%M:%S")) + ",")
        final_config += SafeString("end:" + "'{}-{}T{}'".format(event.end.year, event.end.strftime("%m-%d"), event.end.strftime("%H:%M:%S")) + ",},")
    final_config += SafeString("],}")

    return final_config

@register.simple_tag
def get_event_list():
    events = CalendarEvent.objects.all()
    event_list = SafeString("<ul>")
    for event in events:
        event_list += SafeString("<li>{}</li>".format(event.title))
    event_list += SafeString("</ul>")

    return event_list

@register.simple_tag
def get_category_url(value):
    category = Category.objects.get(slug=value)
    return category.get_absolute_url()
