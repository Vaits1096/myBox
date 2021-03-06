from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, UserAdminCreationForm
from boxApp.models import Coach, Athlete, Box

# Create your views here.
from django.shortcuts import render, redirect

def index(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_admin:
            profile = get_object_or_404(Coach, user = request.user)
        else:
            profile = get_object_or_404(Athlete, user = request.user)
        context['user'] = profile
    return render(request, "accounts/index.html", context)

def welcome(request):
    # Si estamos identificados devolvemos la portada
    user = None
    box = None
    if request.user.is_authenticated:
        if request.user.is_admin:
            profile = get_object_or_404(Coach, user = request.user)
        else:
            profile = get_object_or_404(Athlete, user = request.user)
        if profile is not None:
            box = profile.box
            return render(request, "boxApp/index.html", { 'user': request.user, 'profile': profile, 'box': box})
    # En otro caso redireccionamos al login
    return redirect('../accounts/login')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserAdminCreationForm()
    form.fields['email'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserAdminCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Obtenemos el entrenador que va a realizar el alta 
            coach = Coach.objects.filter(user = request.user)

            # Obtenemos al box que pertenece
            box = coach.box

            # Creamos el atleta
            ath = Athlete(user, box, "", "", "")

            # Si el usuario y el atleta se crean correctamente 
            if user is not None and ath is not None:
                # Hacemos el login manualmente
                # do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('../../dashboard')

    # Si llegamos al final renderizamos el formulario
    return render(request, "accounts/register.html", {'form': form})

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('../../box')

    # Si llegamos al final renderizamos el formulario
    return render(request, "accounts/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('../../box')