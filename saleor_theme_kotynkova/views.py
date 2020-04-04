from random import randint

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.conf import settings

from saleor.checkout.forms import CountryForm
from saleor.core.utils import get_paginator_items, get_user_shipping_country
from saleor.dashboard.views import staff_member_required
from saleor.account.models import User
from saleor.product.models import Category, Attribute, Product, ProductVariant, AttributeValue
from saleor.product.utils import products_with_details, products_for_products_list, get_product_list_context
from saleor.product.filters import ProductCategoryFilter
from saleor.graphql.decorators import permission_required
from .models import Reservation
from .emails import send_create_reservation_to_customer, send_create_reservation_to_staff
from .filters import ReservationFilter


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
        filtered_variants = ProductVariant.objects.filter(
            name__in=[i.name for i in AttributeValue.objects.filter(id__in=variants)])
        products = products.filter(variants__in=filtered_variants).distinct()

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


def create_reservation(request):
    res_url_generated_id = str(
        str(randint(1000, 9999)) + "-" + str(randint(10000, 99999)) + "-" + str(randint(100000, 999999)))
    for res in Reservation.objects.all():
        if res.slug_id == res_url_generated_id:
            res_url_generated_id = str(
                str(randint(1000, 9999)) + "-" + str(randint(10000, 99999)) + "-" + str(randint(100000, 999999)))
    product_name = request.POST.get('product_name')
    product_id = request.POST.get('product_id')
    user_name = request.POST.get('given_name') + request.POST.get('family_name')
    user_email = request.POST.get('email')
    user_phone = request.POST.get('phone_number')
    user_country = request.POST.get('country')
    user_note = request.POST.get('note')
    product = Product.objects.get(name=product_name, id=product_id)
    staff = User.objects.filter(is_staff=True)[0]
    if product is not None:
        reservation = Reservation.objects.create(slug_id=res_url_generated_id, product_id=product_id,
                                                 product_name=product_name, user=request.user, note=user_note)
        # mail to staff
        send_create_reservation_to_staff.delay(request.user.id)
        # mail to customer
        send_create_reservation_to_customer.delay(request.user.id)

    return redirect('account:details')


def remove_reservation(request):
    slug_id = request.POST.get('res_slug_id')
    res = Reservation.objects.get(slug_id=slug_id)
    if res is not None:
        # mail to admin
        subject, from_email, to = 'Reservation was removed - {}'.format(
            res.product_name), settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER
        html_content = """<h3>Reservation was removed.</h3>
                          <ul>
                            <li><a href="http://{}/dashboard/products/{}/">picture removed from reservation: {}</a></li>
                            <li>email: {}</li>
                          </ul>
                          <p><a href="http://{}/dashboard/orders/reservations/">View reservations in dashboard admin</a>.</p>\
                        """.format(request.site, res.product_id, res.product_name, request.user.email,
                                   request.site)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # mail to guest
        to = request.user.email
        html_content = """<h3>Reservation was removed.</h3>
                          <ul>
                            <li><a href="http://{}/cs/products/category/vsechny-obrazy-1/#slick-slide-{}">picture removed from reservation: {}</a></li>
                            <li>email: {}</li>
                          </ul>
                          <p><a href="http://{}/cs/account/">View reservations in your account</a>.</p>\
                        """.format(request.site, res.product_id, res.product_name, request.user.email,
                                   request.site)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        res.delete()
    return redirect('account:details')


def reserve_picture(request, slug, product_id):
    products = products_with_details(user=request.user)
    product = get_object_or_404(products, id=product_id)
    default_country = get_user_shipping_country(request)
    print(default_country)
    country_form = CountryForm(initial={'country': default_country})
    reservations = None
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(user=request.user)
    is_reserved = False
    reservation_got = None
    if request.user.is_authenticated:
        for res in reservations:
            if res.product_name == product.name:
                is_reserved = True
                reservation_got = Reservation.objects.get(product_name=product.name)
                break
    ctx = {
        'product': product,
        'country_form': country_form,
        'is_reserved': is_reserved,
        'reservation': reservation_got
    }
    return TemplateResponse(request, 'order/reservation.html', ctx)


def reservation_details(request, slug_id):
    reservation = Reservation.objects.get(slug_id=slug_id)
    print(reservation.product_name)
    product = Product.objects.get(name=reservation.product_name)
    ctx = {
        'reservation': reservation,
        'product': product
    }
    return TemplateResponse(
        request, 'account/reservation_details.html', ctx)


@staff_member_required
def reservation_list(request):
    orders = Reservation.objects.prefetch_related('user')
    order_filter = ReservationFilter(request.GET, queryset=orders)
    orders = get_paginator_items(
        order_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {
        'orders': orders, 'filter_set': order_filter,
        'is_empty': not order_filter.queryset.exists()}
    return TemplateResponse(request, 'dashboard/order/reservation_list.html', ctx)
