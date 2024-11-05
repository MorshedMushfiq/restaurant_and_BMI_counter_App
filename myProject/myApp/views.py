from django.shortcuts import render,redirect

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
        contact_no=request.POST.get("contact_no")
        Profile_Pic=request.FILES.get("Profile_Pic")
    
        
        if password==Confirm_password:
            
            
            user=CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                Profile_Pic=Profile_Pic,
                contact_no=contact_no,
            )
            if user_type=='seller':
                SellerProfileModel.objects.create(user=user)
                
            elif user_type=='recruiter':
                CustomerProfileModel.objects.create(user=user)
            
            return redirect("signInPage")
            
    return render(request,"common/signupPage.html")


def signInPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return redirect('homePage') 
            else:
                return redirect('signInPage')

        except CustomUser.DoesNotExist:
            return redirect('signInPage')

    return render(request, 'common/signInPage.html')

def homePage(request):
    
    
    return render(request,"common/homePage.html")


def about(request):
    
    
    return render(request,"common/about.html")

def contact(request):
    
    
    return render(request,"common/contact.html")

def blog(request):
    
    
    return render(request,"common/blog.html")

def menu(request):
    
    
    return render(request,"common/menu.html")


def logoutPage(request):
    
    logout(request)
    
    return redirect('signInPage')

@login_required
def profilePage(request):
    
    return render(request,"common/profilePage.html")

@login_required
def editProfile(request):

    if request.method=='POST':
        
        current_user = request.user
        
        current_user.username=request.POST.get("username")
        current_user.email=request.POST.get("email")
        current_user.contact_no=request.POST.get("contact_no")
        new_image = request.FILES.get("new_profile_pic")
        old_image = request.POST.get('old_profile_pic')
        if new_image:
            current_user.Profile_Pic = new_image
        else:
            current_user.Profile_Pic = old_image
        current_user.save()
        return redirect("profilePage")
    
    return render(request,"common/editProfile.html")
