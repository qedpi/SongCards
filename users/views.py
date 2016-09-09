from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import View
from .forms import UserForm
from cards.models import Card
from cards.views import cards_in_row
# Create your views here.

def index(request):
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'users/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                cards = Card.objects.filter(user=request.user).order_by('review_time')[:cards_in_row]
                return render(request, 'cards/index.html', {'cards': cards})
            else:
                return render(request, 'users/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'users/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'users/login.html')
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                cards = Card.objects.filter(user=request.user)
                #return render(request, 'cards/index.html', {'albums': albums})
                return render(request, 'cards/index.html', {'cards': cards})
    else:
        context = {
            "form": form,
        }
        return render(request, 'users/register.html', context)