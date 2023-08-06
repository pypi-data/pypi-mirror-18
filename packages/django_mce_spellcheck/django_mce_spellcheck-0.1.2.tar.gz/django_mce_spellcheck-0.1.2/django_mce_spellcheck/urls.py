from django.conf.urls import url

from django_mce_spellcheck import views

urlpatterns = [
    url(r'^$', views.spellcheck, name='spellcheck'),
]
