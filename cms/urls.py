from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^account/$',
            views.ManagecourseListView.as_view(),
            name='manage_course_list'),
        url(r'^create/$',
            views.courseCreateView.as_view(),
            name='course_create'),
        url(r'^(?P<pk>\d+)/edit/$',
            views.courseUpdateView.as_view(),
            name='course_edit'),
        url(r'^(?P<pk>\d+)/delete/$',
            views.courseDeleteView.as_view(),
            name='course_delete'),
        url(r'^(?P<pk>\d+)/module/$',
            views.courseModulUpdateView.as_view(),
            name='course_course_update'),
        url(r'^module/(?P<course_id>\d+)/content/(?P<model_name>\w+)/create/$',
            views.KontenCreateUpdateView.as_view(),
            name='course_content_create'),
        url(r'^module/(?P<course_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$',
            views.KontenCreateUpdateView.as_view(),
            name='course_content_update'),
        url(r'^content/(?P<id>\d+)/delete/$',
            views.KontenDeleteView.as_view(),
            name='course_content_delete'),
        url(r'^module/(?P<course_id>\d+)/$',
            views.ModulKontenListView.as_view(),
            name='course_content_list'),
        ]