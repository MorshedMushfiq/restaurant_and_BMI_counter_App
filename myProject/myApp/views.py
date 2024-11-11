from django.shortcuts import render,redirect, get_object_or_404

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
        contact_no=request.POST.get("contact_no")
        Profile_Pic=request.FILES.get("Profile_Pic")
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        activity_level = request.POST.get('activity_level')
    
        
        if password==Confirm_password:
            
            
            user=CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                Profile_Pic=Profile_Pic,
                contact_no=contact_no,
                age=age,
                gender=gender,
                activity_level=activity_level
            )
            if user_type=='seller':
                SellerProfileModel.objects.create(user=user)
                
            elif user_type=='customer':
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
        current_user.age=request.POST.get("age")
        current_user.activity_level=request.POST.get("activity_level")

        new_image = request.FILES.get("new_profile_pic")
        old_image = request.POST.get('old_profile_pic')
        if new_image:
            current_user.Profile_Pic = new_image
        else:
            current_user.Profile_Pic = old_image
        current_user.save()
        return redirect("profilePage")
    
    return render(request,"common/editProfile.html")


def allFoods(req):
    foods = Food.objects.filter(is_available=True)
    return render(req, "common/allFoods.html", {'foods': foods})



def addFood(req):
    if req.user.user_type == "seller":  
        if req.method == 'POST':
            # Get data from the form
            name = req.POST.get('name')
            description = req.POST.get('description')
            calories = req.POST.get('calories')
            price = req.POST.get('price')
            is_available = req.POST.get('is_available') == 'on'
            image = req.FILES.get('image')

            # Create a new Food item and save it to the database
            Food.objects.create(
                user = req.user,
                name=name,
                description=description,
                calories=calories,
                price=price,
                is_available=is_available,
                image=image,
            )
            
            # Send a success message
            messages.success(req, 'Food item added successfully!')
            return redirect('manageFood')  # Redirect to the add_food page or another page
        return render(req, 'common/addFood.html')

def manageFood(req):
    if req.user.user_type == "seller":  
        foods = Food.objects.filter(user=req.user)
        return render(req, 'common/manageFood.html', {'foods':foods})
    
def manageOrders(req):
    if req.user.user_type == "seller":
        # Fetch orders for the current seller (food owner)
        food_items = Food.objects.filter(user=req.user)  # Get the food items owned by the seller
        orders = OrderItem.objects.filter(food__in=food_items)  # Get orders for the food items sold by the seller

        if req.method == 'POST':
            order_item_id = req.POST.get('order_id')
            status = req.POST.get('status')

            try:
                order_item = OrderItem.objects.get(id=order_item_id)  # Fetch the order item
                order = order_item.order  # Access the related Order instance
                order.is_delivered = status  # Update the status (delivered, pending, cancel)
                order.save()  # Save the updated order
                messages.success(req, "Food Status Updated Successfully!")
            except OrderItem.DoesNotExist:
                messages.warning(req, "Something went wrong with the order!")
                pass  # Handle case where order item does not exist (optional)

            return redirect('manageOrders')

        return render(req, 'common/manageOrders.html', {'orders': orders})

# Detail view for a single food item
def foodDetail(request, id):
    food = get_object_or_404(Food, id=id)
    return render(request, 'common/foodDetails.html', {'food': food})

# Edit view for a food item
def foodEdit(request, id):
    food = get_object_or_404(Food, id=id)
    if request.method == 'POST':
        food.id = request.POST.get('food_id')
        food.name = request.POST.get('name')
        food.description = request.POST.get('description')
        food.calories = request.POST.get('calories')
        food.price = request.POST.get('price')
        food.is_available = request.POST.get('is_available') == 'on'
        old_img = request.POST.get('old_img')
        new_img = request.FILES.get('new_img')

        if new_img:
            food.image = new_img
        else:
            food.image = old_img
        

        food.save()
        
        messages.success(request, 'Food item updated successfully!')
        return redirect('manageFood')
    
    return render(request, 'common/foodEdit.html', {'food': food})

# Delete view for a food item
def foodDelete(request, id):
    food = get_object_or_404(Food, id=id)
    food.delete()
    messages.success(request, 'Food item deleted successfully!')
    return redirect('manageFood')




# View for single food page
def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    total_calories = 0
    total_price = 0

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Calculate the total calories based on the quantity
        total_calories = food.calories * quantity
        total_price = food.price * quantity

        # Add to cart
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, food=food)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'{food.name} added to your cart.')
            return redirect('view_cart')
        else:
            messages.error(request, 'You need to be logged in to add items to your cart.')

    return render(request, 'common/food_detail.html', {'food': food, 'total_calories':total_calories, 'total_price':total_price})





# Add item to cart
@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, food=food)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{food.name} added to cart!")
    return redirect('view_cart')

# View cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)  # Updated calculation for total price
    return render(request, 'common/cart.html', {'cart_items': cart_items, 'total_price': total_price,})

# Update quantity of item in cart
@login_required
def update_cart_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        
        # Ensure quantity is at least 1
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.food.name} to {new_quantity}.")
        else:
            messages.error(request, "Quantity must be at least 1.")
    
    return redirect('view_cart')  # Redirect back to the cart page after updating

# Remove item from cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    
    # Delete the item from the cart
    cart_item.delete()
    messages.success(request, f"{cart_item.food.name} has been removed from your cart.")
    
    return redirect('view_cart')  # Redirect back to the cart page after removing the item



# Place order
@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Calculate the total price from cart items
    total_price = sum(item.get_total_price() for item in cart_items)

    # Create order
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.save()

    # Create OrderItems based on CartItems
    for cart_item in cart_items:
        OrderItem.objects.create(
            user=request.user,
            order=order,
            food=cart_item.food,
            quantity=cart_item.quantity
        )

    # Clear the cart after placing the order
    cart_items.delete()

    messages.success(request, "Order placed successfully!")
    return redirect('orderedFood')

# View order summary
@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
        # Get all OrderItem instances related to this order
    order_items = order.Order.all()  # Using the related_name defined in OrderItem model

    return render(request, 'common/order_summary.html', {'order': order, 'order_items': order_items})






# View ordered food
@login_required
def orderedFood(request):
    if request.user.user_type == "customer":
        orders = Order.objects.filter(user=request.user).prefetch_related('Order')
        return render(request, 'common/orderedFood.html', {'orders': orders})
   
   # Order Details View (Single View)
@login_required
def singleOrder(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        # Get all OrderItem instances related to this order
        order_items = order.Order.all()  # Using the related_name defined in OrderItem model

    except Order.DoesNotExist:
        messages.error(request, "Order not found or you do not have permission to view this order.")
        return redirect('orderedFood')  # Redirect to orders list if not found or unauthorized

    return render(request, 'common/singleOrder.html', {'order':order, 'order_items':order_items,})



# Cancel order
@login_required
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.is_delivered == "delivered":
            messages.error(request, "You cannot cancel an order after it has been delivered.")
        else:
            order.delete()
            messages.success(request, "Your order has been canceled.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found or you do not have permission to cancel this order.")
    return redirect('orderedFood')



# Function to get the recommended calorie intake
def get_recommended_calories(age, gender, activity_level):
    # Recommended values from the chart
    recommended_calories = {
        'men': {
            'sedentary': {18: 2400, 26: 2400, 46: 2200, 65: 2000},
            'moderately_active': {18: 2800, 26: 2600, 46: 2400, 65: 2200},
            'very_active': {18: 3000, 26: 2800, 46: 2600, 65: 2400},
        },
        'women': {
            'sedentary': {18: 1800, 26: 1800, 46: 1800, 65: 1600},
            'moderately_active': {18: 2100, 26: 2000, 46: 2000, 65: 1800},
            'very_active': {18: 2400, 26: 2200, 46: 2200, 65: 2000},
        },
    }

    # Get the correct recommended value based on age, gender, and activity level
    if gender == 'male':
        for age_group in recommended_calories['men'][activity_level]:
            if age >= age_group:
                recommended_value = recommended_calories['men'][activity_level][age_group]
    else:
        for age_group in recommended_calories['women'][activity_level]:
            if age >= age_group:
                recommended_value = recommended_calories['women'][activity_level][age_group]

    return recommended_value




@login_required
def calorie_counter(request):
    calorie_items = CalorieCounter.objects.filter(user=request.user)
    
    # Handle empty calorie_items list gracefully
    total_calories = sum(item.get_total_calories() for item in calorie_items if item.quantity)
     # Assuming user profile has fields for age, gender, and activity level
    user_profile = request.user
    recommended_calories = get_recommended_calories(user_profile.age, user_profile.gender, user_profile.activity_level)

    # Check if the user has exceeded their recommended calories
    overloaded = total_calories > recommended_calories

    # Get all available food items
    food_items = Food.objects.all()

    return render(request, 'common/calorieCounter.html', {
        'food_items': calorie_items,
        'total_calories': total_calories,
        'all_food_items': food_items,  # Available food items
        'overloaded':overloaded,
    })

@login_required
def add_food_to_counter(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Ensure quantity is always a number

        # Add food to calorie counter with the specified quantity
        calorie_counter_item, created = CalorieCounter.objects.get_or_create(
            user=request.user,
            food=food
        )
        
        calorie_counter_item.quantity = quantity
        
        calorie_counter_item.save()


    return redirect('calorie_counter')

# Remove food item from the calorie counter
@login_required
def remove_food_from_counter(request, food_item_id):
    food_item = get_object_or_404(CalorieCounter, id=food_item_id, user=request.user)
    food_item.delete()
    messages.success(request, "Food has been removed from your calorie counter.")
    return redirect('calorie_counter')