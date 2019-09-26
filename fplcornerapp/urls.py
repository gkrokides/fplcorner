from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^player-comparison$', views.player_comparison, name='player_comparison'),
    url(r'^discover-value$', views.discover_value, name='discover_value'),
    url(r'^testview$', views.testview, name='testview')

]
