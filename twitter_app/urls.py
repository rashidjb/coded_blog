from django.conf.urls import url, include
from . import views

urlpatterns = [

	url(r'^test/$', views.twitter_test, name="test"),


]