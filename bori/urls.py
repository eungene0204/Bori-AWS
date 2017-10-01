from django.conf.urls import url
from bori import views


urlpatterns = [
    url(r'^$', views.hello )
]