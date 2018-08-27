import json

from django.template import Library
from django.utils.http import urlencode
from saleor.product.models import Collection

register = Library()

@register.inclusion_tag('product/product_collection.html')
def collection_prodcuts(collection_slug, template_style):
    collection = Collection.objects.get(slug=collection_slug)
    return {
        'product_list': collection.products.all,
        'template_style': template_style,
        }

@register.filter(name='count_products')
def count_products(value):
    counted = 0
    for product, availability in value:
        if product:
            counted += 1
    return counted
