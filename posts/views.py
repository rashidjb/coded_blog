from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, UserSignUp, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
 

def usersignup(request):
	context = {}
	form = UserSignUp()
	context["form"] = form
	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = user.username
			password = user.password
			user.set_password(password)
			user.save()
			auth_user = authenticate(username = username, password = password)
			login(request, auth_user)

			return redirect("posts:list")
		messages.warning(request, form.errors)
		return redirect("posts:signup")
	return render(request, "signup.html", context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context["form"] = form
	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username = username, password = password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("posts:list")
			messages.warning(request, "Wrong login details, please try again")
			return redirect("posts:list")
		messages.warning(request, form.errors)
		return redirect("posts:login")
	return render(request, "login.html", context)

def userlogout(request):
	logout(request)
	messages.warning(request, "See you later")
	return redirect("posts:list")

def post_home(request):
	return HttpResponse("<h1>Hello</h1>")

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit = False)
		obj.author = request.user
		form.save()
		messages.success(request, "You did it!... eventually.")
		return redirect("posts:list")
	context = {
	'title':'Create',
	'user': request.user,
	'form': form,
	}
	return render(request, 'post_create.html', context)

def post_detail(request, slug):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not (request.user.is_staff or request.user.is_superuser):
			raise Http404
	context = {
	"title": "Detail",
	"instance": instance,
	}
	return render(request, 'post_detail.html', context)
	
def post_list(request):
	today = timezone.now().date()
	object_list = Post.objects.filter(draft = False).filter(publish__lte = today)
	if request.user.is_staff or request.user.is_superuser:
		object_list = Post.objects.all()

	query = request.GET.get("q")

	if query:
		object_list = object_list.filter(
			Q(title__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)|
			Q(content__icontains=query)
			).distinct()

	paginator = Paginator(object_list, 4) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		objects = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)

	context = {
	"objects": objects,
	"title": "List",
	"user": request.user,
	"today": today
	}
	return render(request, 'post_list.html', context)

def post_update(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	post_object = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = post_object) 
	if form.is_valid():
		form.save()
		return redirect("posts:list")
	context = {
	'title':'Update',
	'user': request.user,
	'form': form,
	'post_object': post_object,
	}
	return render(request, 'post_update.html', context)

def post_delete(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	Post.objects.get(slug=slug).delete()
	messages.warning(request, "Goodbye Post")
	return redirect("posts:list")