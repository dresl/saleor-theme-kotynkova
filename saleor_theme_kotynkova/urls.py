from django.conf.urls import url

from . import views

from saleor.urls import non_translatable_urlpatterns

non_translatable_urlpatterns += [
    url(r'^django-admin/', admin.site.urls),
]
