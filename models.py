from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(max_length=100)

    destination = models.CharField(max_length=150)

    travel_date = models.DateField()

    travellers = models.PositiveIntegerField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination


class Destination(models.Model):

    CATEGORY_CHOICES = [
        ('Beach', 'Beach'),
        ('Mountain', 'Mountain'),
        ('City', 'City'),
        ('Adventure', 'Adventure'),
        ('Nature', 'Nature'),
    ]

    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )
    description = models.TextField()
    image_url = models.URLField(max_length=500)
    estimated_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    duration_days = models.PositiveIntegerField(default=3)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.country}"
