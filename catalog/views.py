from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    return render(request, 'catalog/index.html', {'title': 'Skystore'})


def contacts(request):
    return render(request, 'catalog/contacts.html', {'title': 'Skystore'})
