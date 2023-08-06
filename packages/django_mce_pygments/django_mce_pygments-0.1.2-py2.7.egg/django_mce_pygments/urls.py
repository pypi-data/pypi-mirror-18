from django.conf.urls import url

from django_mce_pygments import views

urlpatterns = [
    url(r'^renderer/$', views.pygments, name='pygments'),
]
