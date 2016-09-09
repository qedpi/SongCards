from django.conf.urls import url
from . import views

app_name = 'cards'

urlpatterns = [
    #url(r'.*', views.IndexView.as_view(), name='index'),
    #url(r'^$', views.login_user, name='login_user'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_card/', views.CardCreate.as_view(), name='create_card'),
    url(r'^(?P<pk>[\d]+)/update/$', views.CardUpdate.as_view(), name='update_card'),
    url(r'^review/(?P<pk>[\d]+)/(?P<action>[\D]+)$', views.review_card, name='review_card'),
    url(r'^delete/(?P<pk>[\d]+)/$', views.CardDelete.as_view(), name='delete_card'),
    url(r'^(?P<pk>[\d]+)/$', views.DetailView.as_view(), name='detail'),
]
