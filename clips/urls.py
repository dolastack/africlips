from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.videos_list, name='videos_list')
]
