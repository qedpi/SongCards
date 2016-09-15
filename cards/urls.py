from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'cards'

urlpatterns = [
    # Friends and other users
    url(r'^friends/$', views.UserFriendListView.as_view(), name='user_friends_list'),
    url(r'^befriend/', views.befriend, name='befriend'),
    url(r'^unfriend/', views.unfriend, name='unfriend'),

    # Songcards
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Friend's SongCards
    url(r'^friend/', views.friend_cards, name='friend_index'),
    # Public SongCards
    url(r'^public/', views.PublicView.as_view(), name='public_index'),

    # Create Card
    url(r'^create_card/', views.CreateCard.as_view(), name='create_card'),
    # Update Card
    url(r'^(?P<pk>[\d]+)/update/$', views.CardUpdate.as_view(), name='update_card'),
    # Review Card
    url(r'^review/(?P<pk>[\d]+)/(?P<action>[\D]+)/$', views.review_card, name='review_card'),
    # Delete Card
    url(r'^delete/(?P<pk>[\d]+)/$', views.CardDelete.as_view(), name='delete_card'),
    # Toggle Favorite Card
    url(r'^favorite/', views.toggle_favorite_card, name='toggle_favorite'),
    # Toggle Pin Card
    url(r'^pin/', views.toggle_pin_card, name='toggle_pin'),
    # Card Details
    url(r'^(?P<pk>[\d]+)/', views.DetailView.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)