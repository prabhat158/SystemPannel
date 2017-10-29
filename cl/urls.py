from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cl/create', views.createcl.as_view()),
]
