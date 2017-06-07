from django.contrib import admin
from .models import Video,YoutubeFeed, VideoFeed, YoutubeVideo
from .forms import YoutubeFeedForm
import feedparser
from .tasks import save_video

class VideoFeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

class YoutubeFeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    def save_model(self, request, obj, form, change):
        if request.method == "POST":
            form = YoutubeFeedForm(request.POST)
            if form.is_valid():
                youtube_feed = form.save(commit=False)
                existingFeed = YoutubeFeed.objects.filter(external_id = youtube_feed.external_id)

                if len(existingFeed) == 0:
                    feedData = feedparser.parse(youtube_feed.full_url)
                    youtube_feed.title =  feedData.feed.title
                    youtube_feed.save()
                    save_video(feedData, youtube_feed)

class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'embed_code')
# Register your models here.
admin.site.register(Video)
admin.site.register(VideoFeed , VideoFeedAdmin)
admin.site.register(YoutubeFeed, YoutubeFeedAdmin)
admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
