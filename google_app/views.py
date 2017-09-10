from django.shortcuts import render
from django.http import JsonResponse
import requests

# Create your views here.

def text_search(request):
	api_key = "AIzaSyCI3a_YaooITYXYRuKF7-eJiK9JBA_bZPU"
	query = request.GET.get("place", "")
	next_page_token = request.GET.get("next_page_token")
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s'%(query, api_key)
	if next_page_token:
		url +="&pagetoken=%s"%(next_page_token)
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	return render(request, 'text.html', {'response': response.json()})


def near_search(request):
	api_key = "AIzaSyCI3a_YaooITYXYRuKF7-eJiK9JBA_bZPU"
	next_page_token = request.GET.get("next_page_token")
	lat = request.GET.get("latitude")
	lng = request.GET.get("longitude")
	radius = request.GET.get("radius")

	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=%s&location=%s,%s&radius=%s'%(api_key, lat, lng, radius)
	response = requests.get(url)
	if next_page_token:
		url +="&pagetoken=%s"%(next_page_token)
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	return render(request, 'near.html', {'response': response.json()})


def place_detail(request):
	api_key = "AIzaSyCI3a_YaooITYXYRuKF7-eJiK9JBA_bZPU"
	maps_api_key = "AIzaSyDdd3UPdr6l2bQ5-zz2_jPUzcUQzqIKR-w"
	reference = request.GET.get("reference", "")
	url = 'https://maps.googleapis.com/maps/api/place/details/json?reference=%s&key=%s'%(reference, api_key)
	response = requests.get(url)
	context = {
		'response': response.json(),
		'maps_key': maps_api_key,
	 }
	# return JsonResponse(response.json(), safe=False)
	return render(request, 'detail.html', context )

