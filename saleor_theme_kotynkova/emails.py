from django.urls import reverse
from templated_email import send_templated_mail

from saleor.account.models import User
from saleor.celeryconf import app
from saleor.core.emails import get_email_context
from saleor.core.utils import build_absolute_uri


@app.task
def send_create_reservation_to_staff(customer_pok):
    customer = User.objects.get(pk=customer_pok)
    send_kwargs, ctx = get_email_context()
    ctx["dashboard_url"] = build_absolute_uri(reverse("dashboard:index"))
    send_templated_mail(
        template_name="reservation/staff_create_reservation",
        recipient_list=[customer.email],
        context=ctx,
        **send_kwargs,
    )


@app.task
def send_create_reservation_to_customer(customer_pok):
    customer = User.objects.get(pk=customer_pok)
    send_kwargs, ctx = get_email_context()
    ctx["customer"] = build_absolute_uri(reverse("dashboard:index"))
    send_templated_mail(
        template_name="reservation/customer_create_reservation",
        recipient_list=[customer.email],
        context=ctx,
        **send_kwargs,
    )
