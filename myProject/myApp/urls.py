
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
    path("all_available_oods/", allFoods, name="allFoods"),
    path("add_food/", addFood, name="addFood"),
    path("manage_food/", manageFood, name="manageFood"),
    path("manage_orders/", manageOrders, name="manageOrders"),
    path('foods/<int:id>/', foodDetail, name='foodDetail'),
    path('foods/<int:id>/edit/', foodEdit, name='foodEdit'),
    path('foods/<int:id>/delete/', foodDelete, name='foodDelete'),
    path('food/<int:food_id>/', food_detail, name='food_detail'),
    path("ordered_food/", orderedFood, name="orderedFood"),
    path('single_order/<int:order_id>/', singleOrder, name='singleOrder'),
    path('cart/update_quantity/<int:cart_item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('order/cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('add-to-cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('place-order/', place_order, name='place_order'),
    path('order-summary/<int:order_id>/', order_summary, name='order_summary'),
    path('calorie_counter/', calorie_counter, name='calorie_counter'),
    path('add_food/<int:food_id>/', add_food_to_counter, name='add_food_to_counter'),
    path('remove_food/<int:food_item_id>/', remove_food_from_counter, name='remove_food_from_counter'),

    
    
]