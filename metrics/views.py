from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from operator import itemgetter

from metrics.models import Video, Theme

def get_popular_themes(request):
    theme_list = []

    for theme in Theme.objects.all():
        video_list = Video.objects.filter(theme__id=theme.id)

        score = 0

        for video in video_list:
            time_factor = max(0, 1 - ((timezone.now()-video.date_uploaded).days)/365)

            total_comments = video.comment_set.count()
            positive_comments = video.comment_set.filter(is_positive=True).count()
            negative_comments = total_comments - positive_comments

            total_thumbs = video.thumb_set.count()
            thumbs_up = video.thumb_set.filter(is_positive=True).count()
            thumbs_down = total_thumbs - thumbs_up

            positivity_factor = 0.7 * positive_comments + 0.3 * thumbs_up
            good_comments = positive_comments / (positive_comments / negative_comments) if negative_comments != 0 else 0
            thumbs_up = thumbs_up / (thumbs_up / thumbs_down) if thumbs_down != 0 else 0

            score += video.views * time_factor * positivity_factor

        theme_list.append({
            'id': theme.id,
            'name': theme.name,
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
