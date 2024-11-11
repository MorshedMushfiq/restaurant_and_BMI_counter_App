from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    USER=[
        ('seller','Seller'),
        ('customer','Customer'),
    ]
    user_type=models.CharField(choices=USER,max_length=100,null=True)
    Profile_Pic=models.ImageField(upload_to='Media/Profile_Pic',null=True)
    contact_no=models.CharField(max_length=100,null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=50, null=True)
    activity_level = models.CharField(choices=[('sedentary', 'Sedentary'), ('moderately_active', 'Moderately Active'), ('very_active', 'Very Active')], max_length=50, null=True)
    
    def __str__(self):   
        
        return f"{self.username}"
    
class CustomerProfileModel(models.Model):
    
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='CustomerProfile')

   
    def __str__(self):
        return f"{self.user.username}"
    
    
class SellerProfileModel(models.Model):
    
   
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='SellerProfile')
   
    def __str__(self):
        return f"{self.user.username}"
    
class Food(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Food', null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)  # Optional field for food description
    calories = models.PositiveIntegerField(null=True)  # Store calories as a positive integer
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # Price with 2 decimal places
    is_available = models.BooleanField(default=True, null=True)  # Check if the item is available
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    # Optional: add timestamps for when food is added or updated
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.calories} kcal"
    

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)

    def get_total_price(self):
        return self.quantity * self.food.price
    def get_total_calories(self):
        return self.food.calories * self.quantity
    def __str__(self):
        return f"{self.food.name} - {self.food.calories}Kcal - {self.user.username}"
 
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)
    DELIVERY = [
        ("delivered", "Delivered"),
        ("pending", "Pending"),
        ("cancel", "Cancel"),
    ]
    is_delivered = models.CharField(default="pending", choices=DELIVERY, max_length=50, null=True)

    def __str__(self):
        return f"Order {self.total_price} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='Order', null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)


class CalorieCounter(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_calories(self):
        # Ensure quantity is not None and defaults to 1
        if self.quantity:
            return self.food.calories * self.quantity
        return 0  # Return 0 if no quantity is set

    def __str__(self):
        return f"{self.food.name} (x{self.quantity})"
    
  