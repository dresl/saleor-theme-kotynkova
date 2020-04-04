from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ['created', 'user', 'product_name']
    list_filter = ['created', 'user', 'product_name']
    readonly_fields = ['slug_id', 'created', 'product_id', 'product_name', 'user', 'note']
    search_fields = ['user', 'product_name']


admin.site.register(Reservation, ReservationAdmin)
