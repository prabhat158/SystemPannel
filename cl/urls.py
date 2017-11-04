from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cl/create', views.createcl.as_view()),
    url(r'^contingents', views.getcontingents.as_view()),
    url(r'^contingent/(?P<fb_id>[0-9]+)/createandedit', views.createandeditcontingent.as_view()),
    url(r'^secretcode/approvedminums', views.approvedminumbers.as_view()),
    url(r'^cl/check', views.checkcr.as_view()),
]
