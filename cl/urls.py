from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cl/create', views.createcl.as_view()),
    url(r'^clportal17/check', views.checkcl.as_view()),
    url(r'^clportal17/(?P<google_id>[0-9]+)/createandedit', views.createandeditcontingent.as_view()),
    url(r'^clportal17/(?P<google_id>[0-9]+)/selectmembers', views.selectmembers.as_view()),
    url(r'^clportal17/isapproved/(?P<mi_number>MI-[a-z,A-Z]{2,3}-[0-9]{3,4})$', views.approvedminumbers.as_view()),
    url(r'^clportal17/updatepaidlist', views.updatepaidlist.as_view()),
    url(r'^clportal17/(?P<google_id>[0-9]+)/createmember', views.createmember.as_view()),
    url(r'^clportal17/(?P<pin_code>[0-9]+)/colleges', views.colleges.as_view()),
    url(r'^clportal17/(?P<google_id>[0-9]+)/visit/', views.visit.as_view()),
    url(r'^clportal17/(?P<google_id>[0-9]+)/getcl', views.getcl.as_view()),
    url(r'^clportal17/(?P<google_id>[0-9]+)/getcollege', views.getcollege.as_view()),
    url(r'^clportal17/get_cl', views.getcl_college.as_view()),
    url(r'^clportal17/approvedcl/(?P<mi_number>MI-[a-z,A-Z]{2,3}-[0-9]{3,4})$', views.approvedcl.as_view()),
]

'''
url(r'^contingents', views.getcontingents.as_view()),
url(r'^contingent/(?P<fb_id>[0-9]+)/createandedit', views.createandeditcontingent.as_view()),
url(r'^secretcode/approvedminums', views.approvedminumbers.as_view()),
url(r'^cl/check', views.checkcr.as_view()),
'''

