from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class HashTag(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.CharField(max_length=255, null=True, blank=True)  # Allow image to be null or blank
    created_on = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(HashTag)
    view_count = models.IntegerField(default=0)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
