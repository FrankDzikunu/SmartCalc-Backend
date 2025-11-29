from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

# --- Helper: Only superusers can access ---
def admin_required(view_func):
    decorated_view = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view

# --- Admin Login ---
@csrf_protect
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminpanel:dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # email or username
        password = request.POST.get('password')

        # Try to get username from email if exists
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier

        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('adminpanel:dashboard')
        else:
            messages.error(request, "Invalid credentials or not admin!")

    return render(request, 'adminpanel/admin_login.html')

# --- Admin Logout ---
@login_required
def admin_logout(request):
    logout(request)
    return redirect('adminpanel:admin_login')

# --- Dashboard ---
@admin_required
def dashboard(request):
    users = User.objects.order_by('-date_joined')
    total_users = User.objects.count()
    total_admins = User.objects.filter(is_superuser=True).count()
    regular_count = users.filter(is_superuser=False).count()
    recent_users = User.objects.order_by('-date_joined')[:5]

    context = {
        "total_users": total_users,
        "total_admins": total_admins,
        "recent_users": recent_users,
        "regular_count": regular_count,
    }
    return render(request, 'adminpanel/dashboard.html', context)

# --- List Users ---
@admin_required
def user_list(request):
    users = User.objects.order_by('-date_joined')
    admin_count = users.filter(is_superuser=True).count()
    regular_count = users.filter(is_superuser=False).count()
    return render(request, "adminpanel/user_list.html", {
        "users": users,
        "admin_count": admin_count,
        "regular_count": regular_count,
    }) 


# --- Add Regular User ---
@admin_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin') == 'on'

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_admin,
                is_superuser=is_admin
            )
            messages.success(request, f"User '{username}' created successfully!")
            return redirect('adminpanel:user_list')

    return render(request, 'adminpanel/add_user.html')

# --- Add New Admin ---
@admin_required
def add_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, f'Admin "{username}" created successfully.')
            return redirect('adminpanel:dashboard')

    return render(request, 'adminpanel/add_admin.html')

# --- Delete User ---
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_user = request.user

    # Prevent deleting superuser
    if user.is_superuser:
        messages.error(request, "You cannot delete a superuser!")
        return redirect('adminpanel:user_list')

    # Prevent admin from deleting other admins
    if user.is_staff and not current_user.is_superuser:
        messages.error(request, "Only a superuser can delete other admins!")
        return redirect('adminpanel:user_list')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully!")
        return redirect('adminpanel:user_list')

    return render(request, 'adminpanel/delete_user.html', {'user': user})
