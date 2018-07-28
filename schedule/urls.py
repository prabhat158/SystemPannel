from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schedule/events', views.get_schedule_events.as_view()),
    url(r'^schedule/check', views.get_check.as_view()),
]
