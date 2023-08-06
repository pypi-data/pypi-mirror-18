from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.contact_form_view, name='contact'),
]
