from django.conf.urls import url
from . import views

app_name = 'cards'

urlpatterns = [
    # List of Users
    url(r'^users$', views.UserListView.as_view(), name='user_list'),
    # List of User's Friends
    url(r'^friends$', views.UserFriendListView.as_view(), name='user_friends_list'),
    # Songcards
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Friend's SongCards
    url(r'^friend/(?P<friend_id>[\d]+)/', views.friend_cards, name='friend_index'),

    # Create Card
    url(r'^create_card/', views.CreateCard.as_view(), name='create_card'),
    # Update Card
    url(r'^(?P<pk>[\d]+)/update/$', views.CardUpdate.as_view(), name='update_card'),
    # Review Card
    url(r'^review/(?P<pk>[\d]+)/(?P<action>[\D]+)/$', views.review_card, name='review_card'),
    # Delete Card
    url(r'^delete/(?P<pk>[\d]+)/$', views.CardDelete.as_view(), name='delete_card'),
    # Card Details
    url(r'^(?P<pk>[\d]+)/$', views.DetailView.as_view(), name='detail'),
]
