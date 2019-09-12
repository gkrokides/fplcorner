from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^player-comparison$', views.player_comparison, name='player_comparison')

]
