from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import Friendship
from .models import Card, User

cards_in_row = 4
settings = ['again', 'easy', 'medium', 'hard']
modifiers = [.1, 2, 1.3, 1]
multipliers = dict(zip(settings, modifiers))
used_fields = ['topic', 'front', 'back', 'card_audio', 'card_score', 'card_pic',
               'is_favorite', 'is_pinned']

class IndexView(generic.ListView):
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
        return want.order_by('-is_pinned', 'review_time')[:]
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


class UserListView(generic.ListView):
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

class UserFriendListView(generic.ListView):
    template_name = 'cards/users_friends_list.html'
    context_object_name = 'friends'
    def get_queryset(self):
        query = self.request.GET.get("q")
        #want = User.objects.all()
        want = Friendship.objects.friends_for_user(user=self.request.user)
        return want

    def get_context_data(self, **kwargs): # possible have *args as well, include in both function and below
        context = super(UserFriendListView, self).get_context_data(**kwargs)
        context['shares_with_me'] = Friendship.objects.friends_of_user(user=self.request.user)
        context['users'] = [u for u in User.objects.all()
                            if not Friendship.objects.is_friend_either(u, self.request.user)
                            and u != self.request.user]
        return context


def review_card(request, pk, action):
    card = get_object_or_404(Card, pk=pk)
    prev_time = card.review_time
    duration = int(card.review_interval)
    duration = timedelta(seconds=duration)
    card.review_time = max(prev_time, timezone.now()) + duration
    card.review_interval = max(int(card.review_interval * multipliers[action]), 60)
    card.is_new = False
    card.save()
    cards = Card.objects.filter(user=request.user).order_by('-is_pinned', 'review_time')[:cards_in_row]
    return render(request, 'cards/index.html', {'cards': cards})


class DetailView(generic.DetailView):
    template_name = 'cards/detail.html'
    model = Card

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context



class CreateCard(CreateView):
    model = Card
    fields = used_fields

    def form_valid(self, form):
        card = form.save(commit=False)
        card.user = self.request.user
        card.review_time = datetime.utcnow()
        card.date_created = datetime.utcnow()
        return super(CreateCard, self).form_valid(form)

class CardUpdate(UpdateView):
    model = Card
    fields = used_fields

class CardDelete(DeleteView):
    model = Card
    success_url = reverse_lazy('cards:index')