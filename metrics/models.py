from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100, blank=False, default='Youtube Video')
    date_uploaded = models.DateTimeField()
    views = models.BigIntegerField()

class VideoInteraction(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField()
    video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class Comment(VideoInteraction):
    pass

class Thumb(VideoInteraction):
    pass

class Theme(models.Model):
    name = models.CharField(max_length=100, null=False)
