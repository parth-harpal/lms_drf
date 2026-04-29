from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

@require_http_methods(["GET"])
def register_page(request):
    """Serve the registration page"""
    return render(request, 'register.html', {})

@require_http_methods(["GET"])
def login_page(request):
    """Serve the login page"""
    return render(request, 'login.html', {})

@require_http_methods(["GET"])
def dashboard_page(request):
    """Serve the dashboard page"""
    return render(request, 'dashboard.html', {})