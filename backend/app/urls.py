# backend/app/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('api/rent-ghost/', views.rent_ghost, name='rent_ghost'),
    path('api/process-payment/', views.process_payment, name='process_payment'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/delete-instance/<int:instance_id>/', views.delete_instance, name='delete_instance'),
    path('api/instance/<int:instance_id>/status/', views.check_instance_status, name='check_instance_status'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]