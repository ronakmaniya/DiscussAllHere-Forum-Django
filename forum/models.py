from django.db import models
from django.contrib.auth.models import User

# {{Ronak CE037}} - Category model is implemented by me.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Discussion model is implemented by me. - {{Utsav CE027}}
class Discussion(models.Model):
    category = models.ForeignKey(Category, related_name='discussions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# {{Ronak CE037}} - Comment model is implemented by me.
class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username}'
