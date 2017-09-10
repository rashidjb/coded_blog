from django.conf.urls import url, include
from . import views

urlpatterns = [

	url(r'^test/$', views.org_members, name="test"),
	url(r'^details/$', views.member_details, name="member_details"),
	url(r'^branches/$', views.list_branches, name="branches"),
	url(r'^repos/$', views.list_repos, name="repos"),

]