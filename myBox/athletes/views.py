from django.shortcuts import render, get_object_or_404
from boxApp.models import Athlete, Coach
from boxApp.views import get_type_user

def athlete_list_view(request):
    queryset = Athlete.objects.all()
    profile = get_type_user(request)
    context = {
        "profile": profile,
        "box": profile.box,
        "user": request.user,
        "object_list": queryset
    }
    return render(request, "athletes/athlete_list.html", context)

def athlete_detail_view(request, id):
    obj = get_object_or_404(Athlete, id=id)
    profile = get_type_user(request)
    context = {
        "profile": profile,
        "box": profile.box,
        "user": request.user,
        "object": obj
    }
    return render(request, "athletes/athlete_detail.html", context)