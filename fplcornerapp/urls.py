from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^player-comparison$', views.player_comparison, name='player_comparison'),
    url(r'^discover-value$', views.discover_value, name='discover_value'),
    url(r'^contactus$', views.email, name='contactus'),
    url(r'^success/$', views.success, name='success'),
    url(r'^about/$', views.about, name='about'),
    url(r'^fstats/$', views.fstats, name='fstats'),
    url(r'^test/$', views.test, name='test'),
    url(r'^mstats/$', views.mstats, name='mstats')


]
