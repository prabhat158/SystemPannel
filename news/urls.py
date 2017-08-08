from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news/$', views.NewsView.as_view()),
]
