from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100, blank=False, default='Youtube Video')
    date_uploaded = models.DateTimeField()
    views = models.BigIntegerField()
    theme = models.ManyToManyField('Theme', related_name='themes')

    def __str__(self):
        return self.title

class VideoInteraction(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField()
    video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class Comment(VideoInteraction):
    
    def __str__(self):
        return ("Comment {}".format(self.id))

class Thumb(VideoInteraction):
    def __str__(self):
        return ("Positive? {}".format(self.is_positive))

class Theme(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name
