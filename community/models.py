from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator


# Create your models here.


class Review(models.Model):
    reviewing_user = models.ForeignKey(
        User, related_name='reviews_given', on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(
        User, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(limit_value=5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewing_user.first_name} reviewed {self.reviewed_user.first_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(
        upload_to='community/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def all_comments(self):
        comments = Comment.objects.filter(post=self.id)
        return comments

    def all_likes(self):
        likes = Like.objects.filter(post=self.id).count()
        return likes


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"Like by {self.user} on {self.post.title}"
