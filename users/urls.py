from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/(?P<google_id>[0-9]+)', views.getuser.as_view()),
    url(r'^user/(?P<mi_no>MI-[a-z,A-Z]{2,3}-[0-9]{3,4})', views.get_mino),
    url(r'^user/get', views.get_user.as_view()),
    url(r'^user/check/(?P<google_id>[0-9]+)', views.check.as_view()),
    url(r'^user/create', views.createuser.as_view()),
    url(r'^team/add/(?P<google_id>[0-9]+)', views.add_member.as_view()),
    url(r'^cities/', views.cities.as_view()),
    url(r'^collegeslist/', views.collegeslist.as_view()),
    url(r'^colleges/(?P<city_id>\d+)', views.colleges.as_view()),
    url(r'^team/my_team/(?P<google_id>[0-9]+)', views.my_team.as_view()),
    url(r'^team/add_member/(?P<google_id>[0-9]+)', views.add_member.as_view()),
    url(r'^team/is_leader/(?P<google_id>[0-9]+)', views.is_leader.as_view()),
    url(r'^team/exit_team/(?P<google_id>[0-9]+)', views.exit_team.as_view()),
    url(r'^team/create_team/(?P<google_id>[0-9]+)', views.create_team.as_view()),
    url(r'^team/leader_name/(?P<mi_number>MI-[a-z,A-Z]{2,3}-[0-9]{3,4})', views.leader_name.as_view()),
    url(r'^learningaid', views.aid.as_view()),
]
