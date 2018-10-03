from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^imagica_trip/register', views.book_ticket.as_view()),        
]
