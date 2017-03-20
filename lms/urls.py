from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^account/$',
            views.ManageKursusListView.as_view(),
            name='manage_kursus_list'),
        url(r'^create/$',
            views.KursusCreateView.as_view(),
            name='kursus_create'),
        url(r'^(?P<pk>\d+)/edit/$',
            views.KursusUpdateView.as_view(),
            name='kursus_edit'),
        url(r'^(?P<pk>\d+)/delete/$',
            views.KursusDeleteView.as_view(),
            name='kursus_delete'),
        ]