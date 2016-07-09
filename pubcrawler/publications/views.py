from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("YOU ARE NOW IN THE PUBLICATIONS APP INDEX")
