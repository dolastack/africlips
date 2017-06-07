from django.db import models
import hashlib
import re
# Create your models here.

class VideoFeed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()

class YoutubeFeed(VideoFeed):
    channel = models.CharField(max_length=200)
    external_id = models.CharField(max_length=200)

    @property
    def full_url(self):
        """full youtube feed url with the external_id """
        return self.url + "?channel_id=" + self.external_id

class Video(models.Model):
    video_feed = models.ForeignKey(VideoFeed, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    publication_date = models.DateTimeField()
    url = models.URLField()
    description = models.TextField()
    video_id = models.CharField(max_length=200, primary_key=True)

    def setID(self):
        idm = hashlib.sha1()
        temp = self.title + self.publication_date + self.url
        idm.update(temp.encode())
        self.video_id = idm.hexdigest()

class YoutubeVideo(Video):
    @property
    def embed_code(self):
        regex_str = r'(https:\/\/www.youtube.com\/)watch\?v\=(.+)'
        regex = re.compile(regex_str)
        matches = regex.findall(self.url)
        return matches[0][0] + "embed/" + matches[0][1]
class EmbedVideo(models.Model):
    title =  models.CharField(max_length=200)
    embed_code = models.CharField(max_length=300)
