from django.db import models
from django.utils import timezone #-->to get created_at and updated_at
# Create your models here.
class Post(models.Model):
    creator=models.CharField(max_length=50)
    title= models.CharField()
    body=models.TextField()
    image=models.ImageField(upload_to='posts/images', null=True, blank=True)
    # likes=models.IntegerField(default=0)
    #comments ...
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all()