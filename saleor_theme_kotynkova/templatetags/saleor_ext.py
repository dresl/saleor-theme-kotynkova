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
                    left: 'prev,next,today',
                    center: 'title',
                    right: '',
                },
                firstDay: 1,
                editable: true,
                locale: 'cs',
                eventMouseover: function (calEvent, jsEvent, view) {
                    $(".bubble").html(
                            "<p><b>" + calEvent.title + "</b></p>" +
                            "<p>" + calEvent.description + "</p>"
                            );
                    $(".bubble").css({ top: jsEvent.pageY + 20, left: jsEvent.pageX + 20}).show(200);
                },
                eventMouseout: function (calEvent, jsEvent, view) {
                    $(".bubble").hide();
                },
                eventLimit: true,
                events: [
            """)
    for event in events:
        final_config += SafeString("{" + "title:" + "'{}'".format(event.title) + ",")
        final_config += SafeString("description:" + "'{}'".format(event.description) + ",")
        final_config += SafeString("start:" + "'{}-{}T{}'".format(event.start.year, event.start.strftime("%m-%d"), event.start.strftime("%H:%M:%S")) + ",")
        final_config += SafeString("end:" + "'{}-{}T{}'".format(event.end.year, event.end.strftime("%m-%d"), event.end.strftime("%H:%M:%S")) + ",},")
    final_config += SafeString("],}")

    return final_config

@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)

@register.filter
def is_in(dictionary, key):
    if str(dictionary) in key:
        return True
    else:
        return False

@register.simple_tag
def get_event_list(ongoing, const_coop, year=None):
    events = CalendarEvent.objects.filter(ongoing=ongoing, constant_cooperation=const_coop)
    if year != None:
        events = events.filter(start__year=year)
    event_list = SafeString("<ul>")
    for event in events:
        event_list += SafeString("<li>{}</li>".format(event.title))
    event_list += SafeString("</ul>")
    return event_list

@register.simple_tag
def get_category_url(value):
    category = Category.objects.get(slug=value)
    return category.get_absolute_url()
