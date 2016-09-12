import requests as requests_library

from datetime import datetime, timedelta
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import Friendship
from .models import Card, User

from .intermediary_data import settings, multipliers, used_fields, interactions

cards_in_row = 20


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'cards/index.html'
    context_object_name = 'cards'
    def get_queryset(self):
        query = self.request.GET.get("q")
        want = Card.objects.filter(user=self.request.user)
        if query:
            want = want.filter(
                Q(topic__icontains=query) |
                Q(front__icontains=query)
            )
        return want.order_by('-is_pinned', 'review_time')[:cards_in_row]
'''
class FriendIndexView(generic.ListView):
    template_name = 'cards/index.html'
    context_object_name = 'cards'

    def get_queryset(self, friend_id=None):
        want = Card.objects.filter(user=User.objects.filter(pk=friend_id))
        return want

    def friend_cards(self, request, friend_id):
        want = Card.objects.filter(user=User.objects.filter(pk=friend_id))
        return render(request, 'cards/index.html', {'cards': want})
'''


def friend_cards(request, friend_id):
    want = Card.objects.filter(user=User.objects.filter(pk=friend_id))
    return render(request, 'cards/index.html', {'cards': want})


class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'cards/users_list.html'
    context_object_name = 'users'
    def get_queryset(self):
        query = self.request.GET.get("q")
        want = User.objects.all()
        if query:
            want = want.filter(
                Q(username__icontains=query)
            )
        return want.order_by('username')

class UserFriendListView(LoginRequiredMixin, generic.ListView):
    template_name = 'cards/users_friends_list.html'
    context_object_name = 'shares_with_me'
    def get_queryset(self):
        query = self.request.GET.get("q")
        #want = User.objects.all()
        want = Friendship.objects.friends_of_user(user=self.request.user)
        return want

    def get_context_data(self, **kwargs): # possible have *args as well, include in both function and below
        global interactions
        context = super(UserFriendListView, self).get_context_data(**kwargs)
        context['shared_with'] = Friendship.objects.friends_for_user(user=self.request.user)
        context['unrelated_users'] = [u for u in User.objects.all()
                                      if not Friendship.objects.is_friend_either(u, self.request.user)
                                      and u != self.request.user]
        context['interactions'] = interactions
        return context


@login_required
def review_card(request, pk, action):
    card = get_object_or_404(Card, pk=pk)
    if request.user == card.user:
        prev_time = card.review_time
        duration = int(card.review_interval)
        duration = timedelta(seconds=duration)
        card.review_time = timezone.now() + duration
        card.review_interval = max(int(card.review_interval * multipliers[action]), 60)
        card.is_new = False
        card.save()
    cards = Card.objects.filter(user=request.user).order_by('-is_pinned', 'review_time')[:cards_in_row]
    return render(request, 'cards/index.html', {'cards': cards})


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'cards/detail.html'
    model = Card

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context



class CreateCard(LoginRequiredMixin, CreateView):
    model = Card
    fields = used_fields

    def form_valid(self, form):
        card = form.save(commit=False)
        card.user = self.request.user
        card.review_time = datetime.utcnow()
        card.date_created = datetime.utcnow()

        if card.card_audio != "auto_generate":
            domain, vid = card.card_audio.split('watch?v=')
            card.card_audio = domain + 'embed/' + vid
        else:
            #auto generate
            query_string = card.topic + ' ' + card.front
            youtube_query_format = '+'.join(query_string.split(' '))
            youtube_query_string = "http://www.youtube.com/results?search_query=" + youtube_query_format
            print(youtube_query_string)
            response_html = requests_library.get(youtube_query_string)
            vid_uncleaned = next(re.finditer(r'(clearfix" data-context-item-id=").+? ', response_html.text)).group()
            card.card_audio = "http://www.youtube.com/embed/" + vid_uncleaned.split('"')[2]
            print(vid_uncleaned)

        if card.card_score == "auto_generate":
            domain = "https://tabs.ultimate-guitar.com/"
            artist = '_'.join(card.front.lower().split(' '))
            title = '_'.join(card.topic.lower().split(' ')) + '_crd.htm'
            card.card_score = domain + artist[0] + '/' + artist + '/' + title

        return super(CreateCard, self).form_valid(form)

#add: make user = owner to edit
class CardUpdate(LoginRequiredMixin, UpdateView):
    model = Card
    fields = used_fields

#add: only owner can delete: loginrequired not working right now
class CardDelete(LoginRequiredMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('cards:index')