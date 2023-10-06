from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def logoutUser(request):
    logout(request)
    return redirect('/')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Conta criada com sucesso!!!!')
                return redirect('login')
    context = {'form':form}
    return render(request, 'register.html', context)

def loginUser(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Usuário ou Senha incorreto')
                return render(request, 'login.html', context)

    return render(request, 'login.html', context)
