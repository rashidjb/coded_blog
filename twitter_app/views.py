from django.shortcuts import render
from django.http import JsonResponse
from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1
from urllib.parse import quote
import requests
# Create your views here.

def twitter_test(request):
	user = request.user
	social_account = user.socialaccount_set.get(user = user.id)
	application_token = social_account.socialtoken_set.get(account = social_account.id)
	token = application_token.token
	token_secret = application_token.secret

	social_app = SocialApp.objects.get(provider = twitter_account.provider)
	client_id = social_app.client_id
	client_secret = social_app.secret

	auth = OAuth1(client_id, client_secret, token, token_secret)

	search_stuff = quote("from:m1shaal")
	url = "https://api.twitter.com/1.1/search/tweets.json?q=%s"%(search_stuff)

	response = requests.get(url, auth = auth)

	return JsonResponse(response.json(), safe=False)