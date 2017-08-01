from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
	author = models.ForeignKey(User, default = 1)
	title = models.CharField(max_length=255)
	image = models.ImageField(upload_to="blog_images", null=True, blank=True)
	content = models.TextField()
	draft = models.BooleanField(default = False)
	publish = models.DateField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	slug = models.SlugField(unique = True, null = True)

	def __str__(self):
		return self.title

	def get_abs_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-updated", "-timestamp", "-content", "-title"]

# def create_slug(instance, new_slug=None):
# 	slug = slugify (instance.title)
# 	if new_slug is not None:
# 	    slug = new_slug
# 	qs = Post.objects.filter(slug=slug).order_by("-id")
# 	exists = qs.exists()
# 	if exists:
# 	    new_slug = "%s-%s"%(slug,qs.first().id)
# 	    return create_slug(instance, new_slug=new_slug)
# 	return slug

# def pre_save_post_reciever(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug=create_slug(instance)

def post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title)
        qs = Post.objects.filter(slug = slug).order_by("-id")
        exists = qs.exists()
        if exists:
        	slug = "%s-%s"%(slug, instance.id)
        instance.slug = slug
        instance.save()

post_save.connect(post_reciever,sender=Post)