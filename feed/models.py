from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify


class Post(models.Model):
    """
    Post model.
    """
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='feed_post')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    thumbnail = CloudinaryField('image', default='placeholder')
    listed = models.BooleanField(default=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='post_dislikes', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def children(self):
        return self.comments.filter(parent=None)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Post model.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='commenter',
                                  null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='comment_dislikes',
                                      blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='children')

    def __str__(self):
        return f"{self.commenter}: {self.body}"

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()

    # Use @property to get all children of the comment and set this
    # comment as parent, and set is parent to true/false based on result.
    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
