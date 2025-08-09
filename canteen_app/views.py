from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
from .models import MenuItem, Order, OrderItem, User
from decimal import Decimal
import json
import random
import string

# --- Decorators for Role-Based Access Control ---
def is_student(user):
    return user.is_authenticated and user.role == 'student'

def is_seller(user):
    return user.is_authenticated and user.role == 'seller'

def is_admin(user):
    return user.is_authenticated and user.is_superuser

# --- Public Views ---
def landing_page(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_menu')
        elif request.user.role == 'seller':
            return redirect('seller_dashboard')
        else: # admin
            return redirect('admin:index')
    return render(request, 'canteen_app/landing.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'student':
                return redirect('student_menu')
            elif user.role == 'seller':
                return redirect('seller_dashboard')
            else: # admin
                return redirect('admin:index')
        else:
            return render(request, 'canteen_app/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'canteen_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')

# --- Student Views ---
@login_required
@user_passes_test(is_student)
def student_menu(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    categories = MenuItem.objects.values_list('category', flat=True).distinct()
    context = {
        'menu_items': menu_items,
        'categories': categories,
    }
    return render(request, 'canteen_app/student_menu.html', context)

@login_required
@user_passes_test(is_student)
def checkout_view(request):
    return render(request, 'canteen_app/checkout.html')

@login_required
@user_passes_test(is_student)
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    pickup_time = order.created_at + timezone.timedelta(minutes=15)
    return render(request, 'canteen_app/order_confirmation.html', {'order': order, 'pickup_time': pickup_time})

@login_required
@user_passes_test(is_student)
def order_tracking(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__menu_item'), pk=order_id, user=request.user)
    return render(request, 'canteen_app/order_tracking.html', {'order': order})

@login_required
@user_passes_test(is_student)
def student_orders_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'canteen_app/student_order_history.html', {'orders': orders})

# --- Seller Views ---
@login_required
@user_passes_test(is_seller)
def seller_dashboard(request):
    status_filter = request.GET.get('status', 'all')
    orders = Order.objects.select_related('user').prefetch_related('items__menu_item').all().order_by('-created_at')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    return render(request, 'canteen_app/seller_dashboard.html', {'orders': orders})

@login_required
@user_passes_test(is_seller)
def seller_order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user').prefetch_related('items__menu_item'), pk=order_id)
    for item in order.items.all():
        item.total_price = item.quantity * item.unit_price
    return render(request, 'canteen_app/seller_order_detail.html', {'order': order})

@login_required
@user_passes_test(is_seller)
def seller_menu_management(request):
    return render(request, 'canteen_app/seller_menu_management.html')

# --- API Endpoints ---
@require_POST
@login_required
@user_passes_test(is_student)
def create_order(request):
    try:
        cart_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    
    if not cart_data:
        return JsonResponse({'error': 'Cart is empty.'}, status=400)
        
    with transaction.atomic():
        total_amount = Decimal(0)
        order_items_data = []

        for item_id, item_info in cart_data.items():
            try:
                menu_item = MenuItem.objects.get(pk=item_id, is_available=True)
                item_total = menu_item.price * item_info['quantity']
                total_amount += item_total
                order_items_data.append({
                    'menu_item': menu_item,
                    'quantity': item_info['quantity'],
                    'unit_price': menu_item.price,
                })
            except MenuItem.DoesNotExist:
                return JsonResponse({'error': f'Item {item_info.get("name", item_id)} is no longer available.'}, status=404)

        if total_amount == 0:
             return JsonResponse({'error': 'Cart is empty or contains unavailable items.'}, status=400)

        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        new_order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_amount=total_amount,
            status='pending',
        )

        for item_data in order_items_data:
            OrderItem.objects.create(order=new_order, **item_data)
            
    return JsonResponse({'success': True, 'order_id': new_order.id})

@require_http_methods(['PUT'])
@login_required
@user_passes_test(is_seller)
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, pk=order_id)
    valid_statuses = ['pending', 'preparing', 'ready', 'completed', 'cancelled']
    
    if new_status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status provided.'}, status=400)
    
    if new_status == 'preparing' and order.status != 'pending':
        return JsonResponse({'error': 'Can only change status to "Preparing" from "Pending".'}, status=400)
    if new_status == 'ready' and order.status != 'preparing':
        return JsonResponse({'error': 'Can only change status to "Ready" from "Preparing".'}, status=400)
    if new_status == 'completed' and order.status != 'ready':
        return JsonResponse({'error': 'Can only change status to "Completed" from "Ready".'}, status=400)

    old_status = order.status
    order.status = new_status
    order.save()
    
    OrderStatusHistory.objects.create(
        order=order,
        previous_status=old_status,
        new_status=new_status,
        changed_by=request.user,
    )
    
    return JsonResponse({'success': True, 'new_status': new_status})