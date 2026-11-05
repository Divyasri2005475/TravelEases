from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'customer_name',
            'destination',
            'travel_date',
            'travellers',
            'budget',
            'status'
        ]

        widgets = {
            'travel_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'travellers': forms.NumberInput(
                attrs={'min': 1}
            ),

            'budget': forms.NumberInput(
                attrs={'min': 0, 'step': '0.01'}
            ),
        }

    def clean_travel_date(self):
        from django.utils import timezone

        travel_date = self.cleaned_data['travel_date']

        if travel_date < timezone.localdate():
            raise forms.ValidationError(
                "Travel date cannot be in the past."
            )

        return travel_date

    def clean_travellers(self):
        travellers = self.cleaned_data['travellers']

        if travellers < 1:
            raise forms.ValidationError(
                "At least one traveller is required."
            )

        return travellers
    def clean_budget(self):
        budget = self.cleaned_data['budget']

        if budget < 0:
         raise forms.ValidationError(
            "Budget cannot be negative."
         )

        return budget 