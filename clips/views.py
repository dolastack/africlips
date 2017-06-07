from django.shortcuts import render
from .models import YoutubeVideo, VideoFeed, YoutubeFeed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page

# Create your views here.
import datetime


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def videos_list(request):
    videos_list = YoutubeVideo.objects.all().order_by("-publication_date")

    rowsd = [videos_list[x:x+1] for x in range(0, len(videos_list), 1)]

    paginator = Paginator(rowsd, 20)
    page = request.GET.get('page')

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {'videos': videos}
    template = 'clips/videos_list.html'
    return render(request, template, context)

def get_videos():
    time_delta = datetime.datetime.now() - datetime.timedelta(days=7)
    videos = YoutubeVideo.objects.filter(publication_date__gte = time_delta).order_by("-publication_date")
    return videos
