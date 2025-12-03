import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

# --- Helper: Only admin can access ---
def admin_required(view_func):
    decorated_view = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated_view

# --- Admin Login ---
@csrf_protect
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
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
        if user and user.is_staff:
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
    error_log_path = os.path.join(settings.BASE_DIR, "logs/system_errors.log")

    last_error = None
    if os.path.exists(error_log_path):
        with open(error_log_path, "r") as f:
            lines = f.readlines()
            last_error = lines[-1].strip() if lines else None

    users = User.objects.order_by('-date_joined')
    total_users = User.objects.count()
    total_admins = User.objects.filter(is_staff=True).count()
    regular_count = users.filter(is_staff=False, is_superuser=False).count()
    recent_users = User.objects.order_by('-date_joined')[:5]

    context = {
        "total_users": total_users,
        "total_admins": total_admins,
        "recent_users": recent_users,
        "regular_count": regular_count,
        "last_error": last_error,
    }
    return render(request, 'adminpanel/dashboard.html', context)

# --- List Users ---
@admin_required
def user_list(request):
    all_users = User.objects.order_by('-date_joined')

    # Counts from the full queryset
    admin_count = all_users.filter(is_staff=True, is_superuser=False).count()
    superadmin_count = all_users.filter(is_superuser=True).count()
    regular_count = all_users.filter(is_staff=False, is_superuser=False).count()

    # Pagination
    paginator = Paginator(all_users, 10)  # 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, "adminpanel/user_list.html", {
        "users": users,
        "admin_count": admin_count + superadmin_count,  # total admins
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
                is_superuser= False
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
            user.is_superuser = False
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
        messages.error(request, "You cannot delete a super admin!")
        return redirect('adminpanel:user_list')

    # Prevent admin from deleting other admins
    if user.is_staff and not user.is_superuser and not current_user.is_superuser:
        messages.error(request, "Only a super admin can delete other admins!")
        return redirect('adminpanel:user_list')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully!")
        return redirect('adminpanel:user_list')

    return render(request, 'adminpanel/delete_user.html', {'user': user})
