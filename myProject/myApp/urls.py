
from django.urls import path

from myApp.views import *

urlpatterns = [
    path("", homePage, name="homePage"),
    path("about/", about, name="about"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),
    path("menu/", menu, name="menu"),
    path('register/',signupPage,name="signupPage"),
    path("login/", signInPage, name="signInPage"),
    path("logoutPage/", logoutPage, name="logoutPage"),
    path("ProfilePage/", profilePage, name="profilePage"),
    path("editProfile/", editProfile, name="editProfile"),

    
    
]