from django.conf.urls import urls
from . import views

urlpatterns = [
    url(r'^register/$',
        views.LmsRegistrationView.as_view(),
        name='student_registration'),
]