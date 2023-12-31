from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, EventForm, PurchaseForm, EditPurchase, EditAccount
from django.contrib import messages
from .filters import EventsFilter

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

@login_required
def ownerEvents(request):
    user = request.user 
    events = Event.objects.filter(registrant=user)

    if request.method == 'POST':
        event_id_to_delete = request.POST.get('event_id_to_delete')
        if event_id_to_delete:
            event = Event.objects.all()
            event.delete()
            return redirect('/')


    eventFilter = EventsFilter(request.GET, queryset=events)
    events = eventFilter.qs

    context = {'eventFilter': eventFilter, 'events': events}
    return render(request, 'myEvents.html', context)

@login_required
def eventCreate(request):
    user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False) 
            event.registrant = user  
            event.save()  
            return redirect('ownerEvents')
    else:
        form = EventForm()

    context = {'form': form}
    return render(request, 'eventCreate.html', context)

def eventViewer(request):
    events = Event.objects.all()

    context = {'events': events}
    return render(request, "eventViewer.html", context)

def purchaseTicket(request):
    events = Event.objects.all()
    if request.method == 'POST':
        default_ticket = Ticket.objects.first()
        initial_data = {'ticket': default_ticket.pk, 'quantity': 1}
        form = PurchaseForm(request.POST, initial=initial_data)
        if form.is_valid():
            ticket = form.cleaned_data['ticket']
            quantity = form.cleaned_data['quantity']
            total_price = ticket.price * quantity

            form.cleaned_data['total_price'] = total_price
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()

            return redirect('/')
    else:
        form = PurchaseForm()

    context = {'form': form, 'events': events}
    return render(request, 'purchase.html', context)

@login_required
def ownerTicket(request):
    user = request.user 
    purchases = Purchase.objects.filter(user=user)

    context = {'purchases': purchases}
    return render(request, 'myTickets.html', context)

@login_required
def editTicket(request, pk):
    purchase = Purchase.objects.get(id=pk)

    if purchase.user.num_edit >= 3:
        return render(request, 'maxTransfer.html')

    if request.method == 'POST':
        form = EditPurchase(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            purchase.user.num_edit += 1
            purchase.user.save()
            return redirect('ownerTicket')
    else:
        form = EditPurchase(instance=purchase)

    context = {'form': form}
    return render(request, 'editTicket.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)

    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        form = EditAccount(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditAccount(instance=user)

    return render(request, 'editAccount.html', {'form': form})
