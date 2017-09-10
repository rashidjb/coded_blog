from django.conf.urls import url
from google_app import views


urlpatterns = [
	url(r'^text/$', views.text_search, name="text"),
	url(r'^detail/$', views.place_detail, name="detail"),
	url(r'^near/$', views.near_search, name="near"),
]