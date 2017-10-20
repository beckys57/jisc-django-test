from django.db import models
from django.contrib.auth.models import User

# Signals #
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.contrib.sites.models import Site


class Tag(models.Model):
	text = models.CharField(max_length=64)

	def __str__(self):
		return self.text


class Post(models.Model):
	author = models.ForeignKey(User)
	tags = models.ManyToManyField(Tag, blank=True, related_name="tags")

	title = models.CharField(max_length=256)
	body_text = models.TextField()
	view_count = models.PositiveSmallIntegerField(default=0)
	
	created = models.DateTimeField(auto_now_add=True)

	def increment_view_count(self):
		self.view_count += 1;
		self.save()

	def __str__(self):
		return self.title


@receiver(post_save, sender=Post)
def post_save_blogpost(sender, instance, created, *args, **kwargs):
	""" Send an email when the post is created """
	if created:
		# Define the email data
		recipient = "adric.warth@jisc.ac.uk"
		email_from = "Django.test@example.com"
		subject = "New post: {}".format(instance.title)
		if instance.author.first_name:
			author = "{} {}".format(instance.author.first_name, instance.author.last_name)
		else:
			author = instance.username

		request = None
		relative_url = reverse('posts:view_post', args=[instance.id])
		absolute_url = ''.join(['http://', Site.objects.get_current().domain, relative_url])
		# Prepare the body content
		body_context = {
			'title': instance.title,
			'link': absolute_url,
			'author': author,
		}

		body = """
			{author} has written a new post called "{title}"
			<a href="{link}">Click here</a> to read it.
		""".format(**body_context)

		print body

		email = EmailMultiAlternatives(subject, body, email_from, [recipient])
		email.attach_alternative(body.replace('\r\n', '<br>').replace('\n', '<br>'), "text/html")
		try:
			email.send()
		except:
			pass