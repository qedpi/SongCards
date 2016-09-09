from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Card

from datetime import datetime, timedelta

# Create your views here.

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
        return want.order_by('review_time')[:4]

def review_card(request, pk, action):
    multipliers = {'again': .1, 'easy': 2, 'medium': 1.3, 'hard': 1}
    card = get_object_or_404(Card, pk=pk)
    prev_time = card.review_time
    duration = int(card.review_interval)
    duration = timedelta(seconds=duration)
    card.review_time = max(prev_time, timezone.now()) + duration
    card.review_interval = int(card.review_interval * multipliers[action])
    card.is_new = False
    card.save()
    cards = Card.objects.filter(user=request.user).order_by('review_time')[:3]
    return render(request, 'cards/index.html', {'cards': cards})

class DetailView(generic.DetailView):
    template_name = 'cards/detail.html'
    model = Card

class CardCreate(CreateView):
    model = Card
    fields = 'topic front back card_audio card_score card_pic'.split(' ')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.user = self.request.user
        card.review_time = datetime.utcnow()
        return super(CardCreate, self).form_valid(form)

class CardUpdate(UpdateView):
    model = Card
    fields = 'topic front back card_audio card_score card_pic'.split(' ')

class CardDelete(DeleteView):
    model = Card
    success_url = reverse_lazy('cards:index')