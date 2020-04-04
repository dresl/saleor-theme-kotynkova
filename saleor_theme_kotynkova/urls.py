from django.conf.urls import url
from . import views

app_name = 'theme_kotynkova'

urlpatterns = [
    url(r'^(?P<product_id>[0-9]+)/render-image/$',
        views.render_product_image, name="render_product_image"),
    url(r'^(?P<product_id>[0-9]+)/render-thumb/$',
        views.render_product_thumb, name="render_product_thumb"),
    url(r'^(?P<product_id>[0-9]+)/render-details/$',
        views.render_product_details, name="render_product_details"),
    url(r'^create-reservation/$',
        views.create_reservation, name='create_reservation'),
    url(r'^remove-reservation/$',
        views.remove_reservation, name='remove_reservation'),
    url(r'reservation/(?P<slug_id>[a-z0-9-_]+?)/$',
        views.reservation_details, name='reservation_details'),
    url(r'(?P<slug>[a-z0-9-_]+?)-(?P<product_id>[0-9]+)/reservation/$',
        views.reserve_picture, name='reserve_picture'),
]
