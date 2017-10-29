from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^livewire/create', views.createband.as_view()),
]
