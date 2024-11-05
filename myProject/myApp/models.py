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
    
  