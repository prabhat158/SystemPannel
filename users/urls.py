from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^user/(?P<fb_id>[0-9]+)', views.getuser.as_view()),
    url(r'^user/create', views.createuser.as_view()),
    url(r'^cities/', views.cities.as_view()),
    url(r'^colleges/(?P<city_id>\d+)/', views.colleges.as_view()),
]
