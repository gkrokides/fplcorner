from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.test_view, name='test_view')
    # url(r'^posts$', views.post_list, name='post_list')

]
