from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^results/events', views.get_results_events.as_view()),
]
