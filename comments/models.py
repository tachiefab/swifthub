from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CommentManager(models.Manager):

    def filter_by_instance(self, instance):
        content_type =  ContentType.objects.get_for_model(instance)  
        return self.filter(content_type=content_type, object_id=instance.id)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return f'Comment by {self.user} {self.content_object}'
    
    class Meta:
        ordering = ['-created_at']