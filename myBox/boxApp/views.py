from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm

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


def ejemplo(request):
	return HttpResponse("ejemplo")