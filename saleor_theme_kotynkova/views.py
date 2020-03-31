from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.db.models import Q
from saleor.product.models import Category, DigitalContentUrl, Attribute, ProductVariant
from saleor.product.utils import products_with_details, products_for_products_list, get_product_list_context
from saleor.product.filters import ProductCategoryFilter


def render_product_image(request, product_id):
    products = products_with_details(user=request.user)
    product = get_object_or_404(products, id=product_id)
    ctx = {
        'product': product,
    }
    return render(request, 'product/render_product_image.html', ctx)


def render_product_thumb(request, product_id):
    products = products_with_details(user=request.user)
    product = get_object_or_404(products, id=product_id)
    ctx = {
        'product': product,
    }
    return render(request, 'product/render_product_thumb.html', ctx)


def render_product_details(request, product_id):
    products = products_with_details(user=request.user)
    product = get_object_or_404(products, id=product_id)
    ctx = {
        'product': product,
    }
    return render(request, 'product/render_product_details.html', ctx)


# def reserve_picture(request, slug, product_id):
#     products = products_with_details(user=request.user)
#     product = get_object_or_404(products, id=product_id)
#     default_country = get_user_shipping_country(request)
#     country_form = CountryForm(initial={'country': default_country})
#     reservations = None
#     if request.user.is_authenticated:
#         reservations = Reservation.objects.filter(user=request.user)
#     is_reserved = False
#     reservation_got = None
#     if request.user.is_authenticated:
#         for res in reservations:
#             if res.product_name == product.name:
#                 is_reserved = True
#                 reservation_got = Reservation.objects.get(product_name=product.name)
#                 break
#     ctx = {
#         'product': product,
#         'country_form': country_form,
#         'is_reserved': is_reserved,
#         'reservation': reservation_got
#     }
#     return TemplateResponse(request, 'order/reservation.html', ctx)

def category_index(request, slug, category_id):
    categories = Category.objects.prefetch_related("translations")
    category = get_object_or_404(categories, id=category_id)
    if slug != category.slug:
        return redirect(
            "product:category",
            permanent=True,
            slug=category.slug,
            category_id=category_id,
        )
    # Check for subcategories
    categories = category.get_descendants(include_self=True)
    products = (
        products_for_products_list(user=request.user)
        .filter(category__in=categories)
        .order_by('name')
        .prefetch_related("collections")
        .distinct()
    )
    obraz_attr = Attribute.objects.get(slug="obraz-typ")

    products_count = products.count()

    if request.GET.getlist('variants'):
        variants = request.GET.getlist('variants')
        query_q = ""
        counter = 0
        for variant in variants:
            query_q += "Q(attributes={" + "'{}':'{}'".format(obraz_attr.id,
                                                             variants[counter]) + "})"
            counter += 1
            if len(variants) - counter > 0:
                query_q += "|"
        my_variants = ProductVariant.objects.filter(eval(query_q))
        products = products.filter(variants__in=my_variants).distinct()

    if request.GET.get('name'):
        products = products.filter(name__icontains=request.GET.get('name')).distinct()

    request.GET = request.GET.copy()
    if 'obraz-typ' in request.GET:
        del request.GET['obraz-typ']

    product_filter = ProductCategoryFilter(
        request.GET, queryset=products, category=category
    )
    ctx = get_product_list_context(request, product_filter)
    ctx.update({
        'object': category,
        'project_categories': categories,
        'product_attr': obraz_attr,
        'count_products': "/ {}".format(products_count),
    })
    return TemplateResponse(request, "category/index.html", ctx)
