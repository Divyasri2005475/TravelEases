from django.shortcuts import (render, redirect, get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (login, logout)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Booking
from .forms import BookingForm
from django.contrib.auth import authenticate
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from .models import Destination

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render( request,'register.html',{'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:

            login(request, user)

            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Invalid username or password'
            )

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(
        user=request.user
    )
    total = bookings.count()
    upcoming = bookings.filter(
        status='Confirmed',
         travel_date__gte=timezone.localdate()
    ).count()
    completed = bookings.filter(
        status='Completed'
    ).count()
    cancelled = bookings.filter(
        status='Cancelled'
    ).count()

    context = {
        'total': total,
        'upcoming': upcoming,
        'completed': completed,
        'cancelled': cancelled,
        'recent_bookings': bookings.order_by(
            '-created_at'
        )[:5]
    }

    return render(request,'dashboard.html',context)

@login_required
def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(
                request,
                'Booking added successfully!'
            )
            return redirect('view_bookings')
    else:

        form = BookingForm(initial={
            'destination': request.GET.get('destination', ''),
            'travel_date': request.GET.get('travel_date', ''),
            'travellers': request.GET.get('travellers', 1),
        }) 
    return render(
        request,
        'booking_form.html',
        {
            'form': form,
            'title': 'Add New Booking'
        }
    )

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    )
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    if search:
        bookings = bookings.filter(
            Q(destination__icontains=search) |
            Q(customer_name__icontains=search)
        )
    if status:
        bookings = bookings.filter(
            status=status
        )
    context = {
        'bookings': bookings,
        'search': search,
        'selected_status': status
    }
    return render(
        request,
        'booking_list.html',
        context
    )

@login_required
def edit_booking(request, id):
    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )
    if request.method == 'POST':
        form = BookingForm(
            request.POST,
            instance=booking
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Booking updated successfully!'
            )
            return redirect('view_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(
        request,
        'booking_form.html',
        {
            'form': form,
            'title': 'Edit Booking'
        }
    )

@login_required
def delete_booking(request, id):
    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )
    if request.method == 'POST':
        booking.delete()
        messages.success(
            request,
            'Booking deleted successfully!'
        )
        return redirect('view_bookings')
    return render(
        request,
        'confirm_delete.html',
        {'booking': booking}
    )


def explore_destinations(request):

    destinations = Destination.objects.all().order_by('-featured', 'name')

    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    max_budget = request.GET.get('max_budget', '').strip()

    if search:
        destinations = destinations.filter(
            Q(name__icontains=search) |
            Q(country__icontains=search) |
            Q(description__icontains=search)
        )

    if category:
        destinations = destinations.filter(category=category)

    if max_budget:
        try:
            budget = Decimal(max_budget)

            if budget >= 0:
                destinations = destinations.filter(
                    estimated_budget__lte=budget
                )

        except (InvalidOperation, ValueError):
            pass

    categories = Destination.CATEGORY_CHOICES

    context = {
        'destinations': destinations,
        'categories': categories,
        'search': search,
        'selected_category': category,
        'max_budget': max_budget,
    }

    return render(
        request,
        'explore.html',
        context
    )


def destination_detail(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk
    )
    return render(
        request,
        'destination_detail.html',
        {'destination': destination}
    )
