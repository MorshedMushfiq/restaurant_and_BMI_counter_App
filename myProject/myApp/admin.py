from django.contrib import admin

from myApp.models import *


admin.site.register(CustomUser)
admin.site.register(SellerProfileModel) 
admin.site.register(CustomerProfileModel) 
