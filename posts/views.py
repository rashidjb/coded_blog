from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages

def post_home(request):
	return HttpResponse("<h1>Hello</h1>")

def post_create(request):
	form = PostForm(request.POST or None) 
	if form.is_valid():
		form.save()
		messages.success(request, "You did it!... eventually.")
		return redirect("posts:list")
	context = {
	'title':'Create',
	'user': request.user,
	'form': form,
	}
	return render(request, 'post_create.html', context)

def post_detail(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    context = {
    "title": "Detail",
    "instance": instance
    }
    return render(request, 'post_detail.html', context)
	
def post_list(request):
    object_list = Post.objects.all()
    context = {
    "object_list": object_list,
    "title": "List",
    "user": request.user
    }
    return render(request, 'post_list.html', context)

def post_update(request, post_id):
	post_object = get_object_or_404(Post, id=post_id)
	form = PostForm(request.POST or None, instance = post_object) 
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

def post_delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request, "Goodbye Post")
	return redirect("posts:list")