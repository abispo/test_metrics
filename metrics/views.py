from django.views import generic

from metrics.models import Video, Comment, Theme, Thumb

class VideoListView(generic.ListView):
    model = Video
    paginate_by = 10

class VideoDetailView(generic.DetailView):
    model = Video
