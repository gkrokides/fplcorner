# fplcorner URL Configuration


from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('fplcornerapp.urls')),
    url(r'captcha', include('captcha.urls'))
]
