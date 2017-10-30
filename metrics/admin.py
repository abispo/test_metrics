from django.contrib import admin

from metrics.models import Video, Comment, Thumb, Theme

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Thumb)
admin.site.register(Theme)