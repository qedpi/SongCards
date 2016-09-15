import requests as requests_library

from datetime import datetime, timedelta
import re
from urllib import request as url_request

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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from users.models import Friendship
from .models import Card, User
from .models import initial_review_interval, auto_gen_token
from .serializers import CardSerializer

from .intermediary_data import settings, multipliers, used_fields, interactions, KEYS_MAJOR_MINOR

cards_in_row = 20


def splice_with(s, split_by=' ', join_by='_'):
    return join_by.join(s.split(split_by))

def _get_cards(user, search):
    cards = Card.objects.filter(user=user).order_by('-is_pinned', 'review_time')[:cards_in_row]
    return 'cards/index.html', {'cards': cards, 'time_now': timezone.now(), 'search': search}


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

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        context['search'] = 'User'
        return context
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

class PublicView(LoginRequiredMixin, generic.ListView):
    template_name = 'cards/index.html'
    context_object_name = 'cards'

    def get_queryset(self):
        query = self.request.GET.get("q")
        want = Card.objects.filter(visibility='U').exclude(user=self.request.user)
        if query:
            want = want.filter(
                Q(topic__icontains=query) |
                Q(front__icontains=query)
            )
        return want.order_by('topic')[:cards_in_row]

    def get_context_data(self, **kwargs):
        context = super(PublicView, self).get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        context['search'] = 'Public'
        return context


def friend_cards(request):
    return render(request, *_get_cards(User.objects.get(pk=request.POST.get('other_id')), 'Friend'))

def befriend(request):
    f = Friendship(from_user=request.user, to_user=User.objects.get(pk=request.POST.get('other_id')))
    f.save()
    return redirect('cards:user_friends_list')

def unfriend(request):
    f = Friendship.objects.get(from_user=request.user, to_user=User.objects.get(pk=request.POST.get('other_id')))
    f.delete()
    return redirect('cards:user_friends_list')


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
        interactions[0]['arg'] = [u.from_user for u in self.get_queryset()]
        interactions[1]['arg'] = [u.to_user for u in context['shared_with']]
        interactions[2]['arg'] = context['unrelated_users']

        context['interactions'] = interactions[:]
        return context


def toggle_favorite_card(request):
    target = Card.objects.get(pk=request.POST.get('card_id'))
    target.is_favorite ^= 1
    target.save()
    return redirect('cards:index')

def toggle_pin_card(request):
    target = Card.objects.get(pk=request.POST.get('card_id'))
    target.is_pinned ^= 1
    target.save()
    return redirect('cards:index')


@login_required
def review_card(request, pk, action):
    card = get_object_or_404(Card, pk=pk)
    if request.user == card.user:
        prev_time = card.review_time
        duration = int(card.review_interval)
        duration = timedelta(seconds=duration)
        card.review_time = timezone.now() + duration
        card.review_interval = max(int(card.review_interval + multipliers[action]
                                       * initial_review_interval * (0.5 if card.is_favorite else 1)),
                                   initial_review_interval)
        if multipliers[action] == 0:
            card.review_interval = initial_review_interval

        card.is_new = False
        card.save()
    return redirect('cards:index')


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'cards/detail.html'
    model = Card

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['settings'] = settings
        context['keys'] = KEYS_MAJOR_MINOR
        return context


class CreateCard(LoginRequiredMixin, CreateView):
    model = Card
    fields = used_fields

    def clean_spaces(self, s):
        return ' '.join(word for word in s.strip().split() if word)  # only once space between words

    def get_domain(self, card):
        if not card.front or not card.topic: #impossible
            return ''

        domain = "https://tabs.ultimate-guitar.com/"
        artist = splice_with(card.front.lower())
        title = splice_with(card.topic.lower()) + '_crd.htm'
        return domain + artist[0] + '/' + artist + '/' + title

    def form_valid(self, form):
        card = form.save(commit=False)
        card.user = self.request.user
        card.review_time = datetime.utcnow()
        card.date_created = datetime.utcnow()

        # clean
        card.front = self.clean_spaces(card.front).title()
        card.topic = self.clean_spaces(card.topic).title()
        artist = card.front.lower()
        song_title = card.topic.lower()
        combined_q = artist + ' ' + song_title

        if card.card_audio != auto_gen_token:
            domain, v_id = card.card_audio.split('watch?v=')
            card.card_audio = domain + 'embed/' + v_id
        else:  # auto generate
            yt_domain = "http://www.youtube.com/results?search_query="
            yt_query_str = yt_domain + splice_with(combined_q, join_by='+')
            response_html = requests_library.get(yt_query_str)
            try:
                vid_uncleaned = next(re.finditer(r'(clearfix" data-context-item-id=").+? ', response_html.text)).group()
                card.card_audio = "http://www.youtube.com/embed/" + vid_uncleaned.split('"')[2]

                # now see if artist name or song name is misspelled
                # want = requests_library.get(card.card_audio).json()
                # yt_title = want['title']
                #
                # yt_artist, yt_song_title = (s.strip() for s in want['title'].split('-'))

            except StopIteration:
                card.card_audio = "No matching youtube video found."

        if card.card_score == auto_gen_token:
            card.card_score = self.get_domain(card)
            if not card.card_score:
                card.card_score = "No matching lyrics found."

        if card.back == auto_gen_token:
            domain = self.get_domain(card)
            if domain:
                response_html = requests_library.get(domain)
                if "Oops! We couldn't find that page." in response_html.text:
                    try:
                        query_string = splice_with(combined_q, join_by='+')
                        query = "https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=" + query_string
                        response_html = requests_library.get(query)
                        lyrics_string = next(re.finditer(r'(stripe ).+?(song result)',
                                                         response_html.text, re.DOTALL)).group()

                        new_query = lyrics_string[lyrics_string.find("http"):].split('"')[0]
                        response_html = requests_library.get(new_query)
                    except StopIteration:
                        card.back = "SongCards was unable to find the lyrics online."

                try:
                    lyrics_string = next(re.finditer(r'(js-tab-content).+?(/pre)',
                                                     response_html.text, re.DOTALL)).group()
                    lyrics_string = lyrics_string[23:-19]
                    lyrics_string = lyrics_string.replace("<span>", '').replace('</span>', '')

                    card.back = lyrics_string
                except StopIteration:
                    card.back = "SongCards was unable to find the lyrics online."
            else:
                card.back = "SongCards was unable to find the lyrics online."
        if not card.card_pic: #autogenerate
            domain_head = "https://itunes.apple.com/search?term="
            query = combined_q
            query_converted = splice_with(query, join_by='+')
            domain = domain_head + query_converted

            response_data = requests_library.get(domain)

            def get_artwork(response):
                want = response_data.json()
                return want['results'][0]['artworkUrl100']

            save_as = splice_with(query + ' ' + str(self.request.user.id)) + '.jpg'

            def download_pic(pic_url):
                return url_request.urlretrieve(pic_url, 'media/' + save_as)

            try:
                download_pic(get_artwork(response_data))

                card.card_pic = save_as
            except IndexError:
                pass
        return super(CreateCard, self).form_valid(form)


# add: make user = owner to edit
class CardUpdate(LoginRequiredMixin, UpdateView):
    model = Card
    fields = used_fields


# add: only owner can delete: loginrequired not working right now
class CardDelete(LoginRequiredMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('cards:index')