from django.conf.urls import url

from metrics import views

urlpatterns = [
    url(r'^videos/$', views.VideoListView.as_view(), name='videos'),
    url(r'^video/(?P<pk>\d+)$', views.VideoDetailView.as_view(), name='video-detail')
]