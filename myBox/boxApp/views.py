from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Exercise
from .forms import ExerciseForm


def index(request):
    return render(request, "boxApp/index.html")


def ExerisesList(request):
    exerciselist = Exercise.objects.get(id=1)
    context = {'exlist': exerciselist}
    return render(request, "boxApp/exercises.html", context)


def ejemplo(request):
    return HttpResponse("ejemplo")


class ExercisesPageView(ListView):
    model = Exercise
    template_name = 'boxApp/exercises.html'


def CreateExercise(request):
    print('estoy en views')
    if request.method == 'POST':
        register_form = ExerciseForm(request.POST, request.FILES)
        print(register_form.is_valid())
        print(register_form)
        if register_form.is_valid():
            register_form.save()
            return redirect('../exercises')
    else:
        template_name = 'boxApp/exercisesForm.html'
        register_form = ExerciseForm()
        return render(request, 'boxApp/exercisesForm.html', {'register_form': register_form})
