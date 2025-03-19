from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    username = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now=True)

    def get_comment_count(self):
        return Comment.objects.filter(post_id=self.id).count()
    
    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            content=self.content,
            create_time=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            username=self.username,
            comment_count=self.get_comment_count(),
        )
    

class Comment(models.Model):
    post_id = models.BigIntegerField()
    content = models.TextField()
    username = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            content=self.content,
            create_time=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            username=self.username,
        )
