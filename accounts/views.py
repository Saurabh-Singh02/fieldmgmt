from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import CustomUser, ClientCompany, ClientContact, EngineerProfile
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has the selected role
            if user.role == role:
                login(request, user)
                return redirect('dashboard:redirect_dashboard')
            else:
                messages.error(request, f'You are not registered as a {role}')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('dashboard:home')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import EngineerProfile, ClientCompany, ClientContact
from decimal import Decimal
import uuid
from django.utils.timezone import now

User = get_user_model()

import logging
logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            role = request.POST.get("role")

            if User.objects.filter(username=username).exists():
                messages.error(request, "❌ Username already taken.")
                return render(request, "accounts/register.html")

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role
            )

            group, _ = Group.objects.get_or_create(name=role.capitalize())
            user.groups.add(group)

            if role.lower() == 'engineer':
                EngineerProfile.objects.create(
                    user=user,
                    employee_id=f"ENG-{uuid.uuid4().hex[:8]}",
                    hourly_rate=Decimal('0.00')
                )

            elif role.lower() == 'client':
                company_name = f"{first_name} {last_name}'s Company"
                client_company = ClientCompany.objects.create(
                    name=company_name,
                    contact_email=email
                    # created_at=now(),
                )
                ClientContact.objects.create(
                    user=user,
                    company=client_company,
                    position='Owner',
                    is_primary=True
                )

            login(request, user)
            messages.success(request, f"✅ Account created successfully as {role}.")
            return render(request, "accounts/register.html")

        except Exception as e:
            logger.exception("Error during user registration")  # log to console
            messages.error(request, f"❌ Registration failed: {str(e)}")
            return render(request, "accounts/register.html")

    return render(request, "accounts/register.html")

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')