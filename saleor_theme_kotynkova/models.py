from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from .conf import ReservationStatus


class Reservation(models.Model):
    slug_id = models.CharField(
        verbose_name=u"URL ID", max_length=150, default='')
    product_name = models.CharField("Product Name", max_length=386)
    product_id = models.IntegerField("Product ID")
    created = models.DateTimeField(
        default=timezone.now)
    status = models.CharField(
        max_length=32, default=ReservationStatus.RESERVED,
        choices=ReservationStatus.CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reservations',
        on_delete=models.CASCADE)
    note = models.TextField(max_length="500", blank=True, null=True)

    def get_absolute_url(self):
        return reverse('theme_kotynkova:reservation_details', kwargs={'slug_id': self.slug_id})

    class Meta:
        ordering = ('created', )
