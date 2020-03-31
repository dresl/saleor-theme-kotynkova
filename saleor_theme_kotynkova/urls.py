from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'theme_kotynkova'

urlpatterns = [
    url(r'^(?P<product_id>[0-9]+)/render-image/$',
        views.render_product_image, name="render_product_image"),
    url(r'^(?P<product_id>[0-9]+)/render-thumb/$',
        views.render_product_thumb, name="render_product_thumb"),
    url(r'^(?P<product_id>[0-9]+)/render-details/$',
        views.render_product_details, name="render_product_details"),
]
