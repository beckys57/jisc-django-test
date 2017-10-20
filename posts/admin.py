from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):

	def date_created(self, obj):
		return obj.created.strftime("%d/%m/%Y")

	list_display =  ('title', 'author', 'date_created')
	exclude = ('view_count',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
