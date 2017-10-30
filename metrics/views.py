from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from operator import itemgetter
from datetime import timedelta

from metrics.models import Video, Theme

def get_comments_statistics(video):
    return [
        video.comment_set.count(),
        video.comment_set.filter(is_positive=True).count()
    ]

def get_thumbs_statistics(video):
    return [
        video.thumb_set.count(),
        video.thumb_set.filter(is_positive=True).count()
    ]

def index(request):
    return render(
        request,
        'index.html',
        context = {}
    )

def get_popular_themes(request):
    theme_list = []

    for theme in Theme.objects.all():
        video_list = Video.objects.filter(
            theme__id=theme.id,
            date_uploaded__gte=(timezone.now() - timedelta(days=365))
        )

        score = 0

        for video in video_list:
            time_factor = max(0, 1 - ((timezone.now() - video.date_uploaded).days)/365)

            total_comments, positive_comments = get_comments_statistics(video)
            negative_comments = total_comments - positive_comments

            total_thumbs, thumbs_up = get_thumbs_statistics(video)
            thumbs_down = total_thumbs - thumbs_up

            positivity_factor = 0.7 * positive_comments + 0.3 * thumbs_up
            good_comments = positive_comments / (positive_comments / negative_comments) if negative_comments != 0 else 0
            thumbs_up = thumbs_up / (thumbs_up / thumbs_down) if thumbs_down != 0 else 0

            score += video.views * time_factor * positivity_factor

        theme_list.append({
            'theme': theme.id,
            'name': theme.name,
            'get_absolute_url': theme.get_absolute_url(),
            'score': score 
        })

    theme_list = sorted(theme_list, key=itemgetter('score'), reverse=True)

    return render(
        request,
        'get_popular_themes.html',
        context = {
            'theme_list': theme_list
        }
    )

class VideoListView(generic.ListView):
    model = Video
    paginate_by = 10

class VideoDetailView(generic.DetailView):
    model = Video

class ThemeListView(generic.ListView):
    model = Theme
    paginate_by = 10

class ThemeDetailView(generic.DetailView):
    model= Theme

    def get_context_data(self, **kwargs):
        context = super(ThemeDetailView, self).get_context_data(**kwargs)

        video_list = Video.objects.filter(theme__id=self.kwargs['pk'])
        
        context['total_videos'] = video_list.count
        context['video_list'] = video_list
        
        return context