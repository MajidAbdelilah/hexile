from django.db import models
from django.contrib.auth.models import User

class GhostInstance(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    port = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paypal_order_id = models.CharField(max_length=100)  # Changed from stripe_payment_id
    created_at = models.DateTimeField(auto_now_add=True)
    ghost_instance = models.ForeignKey(GhostInstance, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Payment {self.paypal_order_id} for {self.ghost_instance.name}"