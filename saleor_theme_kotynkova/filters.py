from django import forms
from django.db.models import F, Max, Q
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (
    CharFilter,
    ChoiceFilter,
)

from saleor.core.filters import SortedFilterSet
from .conf import ReservationStatus


class ReservationFilter(SortedFilterSet):
    product_name = CharFilter(
        label=pgettext_lazy(
            'Reservation list filter label', 'Product name'),
        method='filter_by_product_name')
    name_or_email = CharFilter(
        label=pgettext_lazy(
            'Reservation list filter label', 'Customer name or email'),
        method='filter_by_order_customer')
    status = ChoiceFilter(
        label=pgettext_lazy(
            'Reservation list filter label', 'Reservation status'),
        choices=ReservationStatus.CHOICES,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)

    def filter_by_product_name(self, queryset, name, value):
        return queryset.filter(
            Q(product_name__icontains=value))

    def filter_by_order_customer(self, queryset, name, value):
        return queryset.filter(
            Q(user__email__icontains=value) |
            Q(user__default_billing_address__first_name__icontains=value) |
            Q(user__default_billing_address__last_name__icontains=value))
