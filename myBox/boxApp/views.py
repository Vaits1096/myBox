from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "boxApp/index.html")

def ejemplo(request):
	return HttpResponse("ejemplo")