from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Exercise, Coach, Athlete, Token
from .forms import ExerciseForm, create_athlete_form
from accounts.forms import UserAdminCreationForm
import datetime
from accounts.views import welcome
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def get_type_user(request):
    if request.user.is_admin:
        profile = get_object_or_404(Coach, user = request.user)
    else:
        profile = get_object_or_404(Athlete, user = request.user)
    return profile


def index(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = form.clean_email
        password = form.clean_password2
        print(email)
        print(password)
        if form.is_valid():
            return render(request, "boxApp/index.html")
    else:
        form = RegisterForm()
    
    return render(request, 'boxApp/register.html', {'form': form})


def create_user(request):
    if request.user.is_authenticated:
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

                # Obtenemos el entrenador que va a realizar el alta 
                coach = get_object_or_404(Coach, user = request.user)

                # Obtenemos al box que pertenece
                box = coach.box

                # Creamos la nueva cuenta de usuario
                user = form.save()

                # Creamos el atleta asociado al usuario
                ath = Athlete(user = user, box = box, user_name= "prueba", name = "prueba", last_name= "prueba")
                ath.save()

                # Si el usuario y el atleta se crean correctamente 
                if user is not None and ath is not None:
                    # Hacemos el login manualmente
                    # do_login(request, user)
                    # Y le redireccionamos a la portada
                    return redirect('../../box')

        # Si llegamos al final renderizamos el formulario
        return render(request, "boxApp/create_user.html", {'form': form})
    return redirect('../../accounts/login')


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
    if request.user.is_authenticated:
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
            profile = get_type_user(request)
            context = {'user': request.user, 'profile':profile, 'box':profile.box, 'register_form': register_form}
            return render(request, 'boxApp/exercisesForm.html', context)
    return redirect('../../accounts/login')


def activate_account(request):
    if len(request.GET) != 0:
        id_coach = request.GET.get('c_id')
        id_ath = request.GET.get('ath_id')
        token = request.GET.get('token')
        coach = get_object_or_404(Coach, id = id_coach)
        user = coach.user
        ath = get_object_or_404(Athlete, id = id_ath)

        token_generator = PasswordResetTokenGenerator()
        is_valid = token_generator.check_token(user, token)
        
        if is_valid:
            is_valid = Token.objects.filter(athlete=ath, token=token).exists()
            if is_valid:
                form = UserAdminCreationForm()
                form.fields['email'].help_text = None
                form.fields['password1'].help_text = None
                form.fields['password2'].help_text = None
                if request.method == "POST":
                    # Añadimos los datos recibidos al formulario
                    form = UserAdminCreationForm(data=request.POST)
                    # Si el formulario es válido...
                    if form.is_valid():

                        user = form.save()

                        ath.user = user
                        ath.save()

                        token = Token.objects.get(athlete=ath, token=token)
                        token.delete()

                        if user is not None:
                            # Hacemos el login manualmente
                            # do_login(request, user)
                            # Y le redireccionamos a la portada
                            return redirect('../../accounts/login')

                # Si llegamos al final renderizamos el formulario
                return render(request, 'boxApp/activate_account.html', {'form': form})
    return redirect('../../')


def create_athlete(request):
    
    if request.user.is_authenticated:
        form = create_athlete_form()
        if request.method == 'POST':

            form =  create_athlete_form(data=request.POST)

            if form.is_valid():
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(request.user)

                email = request.POST.get('email')
                name = request.POST.get('name')
                last_name = request.POST.get('last_name')

                coach = get_object_or_404(Coach, user = request.user)
                box = coach.box

                c_id = str(coach.id)

                ath = Athlete(user = None, box = box, coach = coach, user_name = "", name = name, last_name = last_name)
                ath.save()

                token_obj = Token(athlete = ath, token = token)
                token_obj.save()

                ath_id = str(ath.id)

                body = render_to_string(
                    'boxApp/email_content.html', {
                        'name': name,
                        'token': token,
                        'c_id': c_id,
                        'ath_id': ath_id
                    },
                )

                email_message = EmailMessage(
                    subject='Mensaje de usuario',
                    body=body,
                    from_email="marcos.ml.1096@gmail.com",
                    to=[email],
                )
                try:
                    email_message.content_subtype = 'html'
                    email_message.send()
                    return redirect('../')
                except Exception:
                    print("Borro atletas")
                    ath.delete()
                    token_obj.delete()
                    return redirect('../') # REDIRECCIONAR A PAGINA DE ERROR
        profile = get_type_user(request)
        context = { 'user': request.user, 'profile': profile, 'box': profile.box, 'form': form}
        return render(request, 'boxApp/create_athlete.html', context)
    return redirect('../../accounts/login')

