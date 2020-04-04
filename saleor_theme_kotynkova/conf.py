from django.utils.translation import pgettext_lazy


class ReservationStatus:
    RESERVED = pgettext_lazy('Reserved status', 'Reserved')
    REJECTED = pgettext_lazy('Rejected status', 'Rejected')
    ACCEPTED = pgettext_lazy('Accepted status', 'Accepted')

    CHOICES = [
        (RESERVED, pgettext_lazy(
            'Status for reservation marked as reserved',
            'Reserved')),
        (REJECTED, pgettext_lazy(
            'Status for reservation marked as rejected',
            'Rejected')),
        (ACCEPTED, pgettext_lazy(
            'Status for reservation marked as accepted',
            'Accepted'))]
