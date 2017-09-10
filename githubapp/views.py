from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
import requests

# Create your views here.

def org_members(request):
	user = request.user
	social_account = user.socialaccount_set.get(user = user.id)
	application_token = social_account.socialtoken_set.get(account = social_account.id)
	token = application_token.token

	url = "http://api.github.com/orgs/joinCODED/members"

	response = requests.get(url, headers={'Authorization': 'token '+token})

	context = {

		"response":response.json()
	}

	return render(request, "members.html", context)

	# return JsonResponse(response.json(), safe=False)

def list_branches(request):
	user = request.user
	social_account = user.socialaccount_set.get(user = user.id)
	application_token = social_account.socialtoken_set.get(account = social_account.id)
	token = application_token.token
	owner = "sentient64"
	repo = "capstone"

	url = "http://api.github.com/repos/"+owner+"/"+repo+"/branches"

	response = requests.get(url, headers={'Authorization': 'token '+token})

	context = {

		"response":response.json(),
		"owner": owner,
		"repo": repo,
	}

	return render(request, "branches.html", context)
	# return JsonResponse(response.json(), safe=False)

def list_repos(request):
	user = request.user
	social_account = user.socialaccount_set.get(user = user.id)
	application_token = social_account.socialtoken_set.get(account = social_account.id)
	token = application_token.token
	owner = request.GET.get("user")
	repo = "capstone"

	url = "http://api.github.com/users/"+owner+"/repos"

	response = requests.get(url, headers={'Authorization': 'token '+token})

	context = {
		"response":response.json(),
		"owner": owner,
	}

	return render(request, "repos.html", context)
	# return JsonResponse(response.json(), safe=False)

def member_details(request):
	user = request.user
	social_account = user.socialaccount_set.get(user = user.id)
	application_token = social_account.socialtoken_set.get(account = social_account.id)
	token = application_token.token
	username = request.GET.get("username")
	url = "http://api.github.com/users/"+username

	response = requests.get(url, headers={'Authorization': 'token '+token})


	context = {

		"response":response.json(),
		"username": username,
	}

	return render(request, "member_details.html", context)
	# return JsonResponse(response.json(), safe=False)