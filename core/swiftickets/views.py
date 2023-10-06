from django.shortcuts import redirect, render
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def logoutUser(request):
    logout(request)
    return redirect('/')