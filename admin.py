from django.contrib import admin
from .models import Booking, Destination


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_name', 'destination', 'travel_date', 'status')
    list_filter = ('status', 'travel_date')
    search_fields = ('customer_name', 'destination')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country',
        'category',
        'estimated_budget',
        'duration_days',
        'featured'
    )
    list_filter = ('category', 'featured', 'country')
    search_fields = ('name', 'country')
    list_editable = ('featured',)