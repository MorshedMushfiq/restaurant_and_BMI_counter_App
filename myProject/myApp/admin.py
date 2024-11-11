from django.contrib import admin

from myApp.models import *


admin.site.register(CustomUser)
admin.site.register(SellerProfileModel) 
admin.site.register(CustomerProfileModel)
admin.site.register(Food)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
