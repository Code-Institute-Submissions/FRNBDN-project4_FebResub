from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT,
                               related_name='feed_post')
    updated_on = models.DateField(auto_now=True)
    created_on = models.DateField(auto_now_add=True)
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

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    if not instance.image == 'placeholder':
        instance.image.delete(False)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='commenter')
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='comment_dislikes',
                                      blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.PROTECT,
                               related_name='children')

    def __str__(self):
        return f"{self.name}: {self.body}"
    
    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()
