from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.CharField(max_length=999)
    timestamp = models.DateTimeField(auto_now_add=True)

    def likes(self):
        return Like.objects.filter(post=self.id).count()

    def serialize(self):
        ap = ""
        T = self.timestamp.strftime("%p")
        if T=="AM": ap = 'a.m.'
        else: ap = 'p.m.' 
        likes = Like.objects.filter(post=self.id).count()
        return {'user':self.user.username,'id': self.id, 'post': self.post, 'timestamp': self.timestamp.strftime("%B %d, %Y, %I:%M ") + ap, 'likes': likes}


class Like(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    post = models.ForeignKey("Post",on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE, related_name='user')
    following = models.ForeignKey("User", on_delete=models.CASCADE)


