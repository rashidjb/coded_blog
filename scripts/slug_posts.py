



from posts.models import Post
from django.template.defaultfilters import slugify

for post in Post.objects.all():
    slug = slugify(post.title)
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
            slug = "%s-%s"%(slug,post.id)
    post.slug=slug
    post.save()