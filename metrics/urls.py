from django.conf.urls import url

from metrics import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^videos/$', views.VideoListView.as_view(), name='videos'),
    url(r'^video/(?P<pk>\d+)/$', views.VideoDetailView.as_view(), name='video-detail'),
    url(r'^themes/$', views.ThemeListView.as_view(), name='themes'),
    url(r'^theme/(?P<pk>\d+)/$', views.ThemeDetailView.as_view(), name='theme-detail'),
    url(r'^get_popular_themes/$', views.get_popular_themes, name='get-popular-themes'),
]