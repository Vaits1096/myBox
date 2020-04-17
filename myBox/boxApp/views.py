from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("My Box app. Lets go!")

def ejemplo(request):
	return HttpResponse("ejemplo")