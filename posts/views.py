from django.shortcuts import render
from .models import Post

# Create your views here.
def list_all(request):
	""" Displays a list of all posts """
	sort = request.GET.get('sort', 'date')
	if sort == 'date':
		order = '-created'
	else:
		order = '-view_count'

	context = {
		'posts': Post.objects.all().order_by(order)
	}
	return render(request, 'posts/list.html', context)


def view_post(request, post_id):
	""" Displays the blog post in full """

	post = Post.objects.get(id=post_id)
	post.increment_view_count()
	print post.view_count
	context = {
		'post': post,
	}
	return render(request, 'posts/view_post.html', context)