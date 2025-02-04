# backend/app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import GhostInstance, Payment
from .utils import InstanceManager
from django.conf import settings
import uuid

logger = logging.getLogger(__name__)
instance_manager = InstanceManager()

def home(request):
    try:
        resp = render(request, 'index.html')
        resp.set_cookie('csrftoken', get_token(request))
        return resp
    except Exception as e:
        logger.exception("Error rendering home page")
        return JsonResponse({'error': 'Home page error.'}, status=500)

def contact(request):
    try:
        return render(request, 'contact.html')
    except Exception as e:
        logger.exception("Error rendering contact page")
        return JsonResponse({'error': 'Contact page error.'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_checkout_session(request):
    try:
        YOUR_DOMAIN = "http://localhost:8000"
        # Use well-wrapped try/except for Stripe API calls
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Your Product Name'},
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        logger.exception("Error creating checkout session")
        return JsonResponse({'error': 'Checkout session creation error.'}, status=500)

def success(request):
    try:
        return render(request, 'success.html')
    except Exception as e:
        logger.exception("Error rendering success page")
        return JsonResponse({'error': 'Success page error.'}, status=500)

def cancel(request):
    try:
        return render(request, 'cancel.html')
    except Exception as e:
        logger.exception("Error rendering cancel page")
        return JsonResponse({'error': 'Cancel page error.'}, status=500)

def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required.'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
@require_http_methods(["POST"])
def rent_ghost(request):
    try:
        instance_name = request.POST.get('instance_name', '').strip()
        if not instance_name:
            return JsonResponse({'error': 'Instance name required.'}, status=400)
        used_ports = GhostInstance.objects.values_list('port', flat=True)
        port = settings.GHOST_BASE_PORT + 1
        while port in used_ports:
            port += 1

        user_obj = request.user if request.user.is_authenticated else None
        ghost_instance = GhostInstance.objects.create(
            name=instance_name, user=user_obj, port=port, status='creating'
        )
        try:
            container_id = instance_manager.create_instance(instance_name, port)
            ghost_instance.container_id = container_id
            ghost_instance.status = 'running'
            ghost_instance.save()
            return JsonResponse({
                'message': 'Instance created.',
                'instance_id': ghost_instance.id,
                'instance_url': ghost_instance.get_url()
            })
        except Exception as e:
            ghost_instance.status = 'error'
            ghost_instance.error_message = str(e)
            ghost_instance.save()
            logger.exception("Docker error")
            return JsonResponse({'error': 'Error creating container.'}, status=500)
    except Exception as e:
        logger.exception("Error processing rent_ghost")
        return JsonResponse({'error': 'Internal error in rent_ghost.'}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def process_payment(request):
    try:
        amount_str = request.POST.get('amount', '').strip()
        instance_id = request.POST.get('instance_id', '').strip()
        if not (amount_str and instance_id):
            return JsonResponse({'error': 'Required parameters missing.'}, status=400)
        try:
            amount = float(amount_str)
            instance_id = int(instance_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid parameter formats.'}, status=400)
        try:
            ghost_instance = GhostInstance.objects.get(id=instance_id)
        except GhostInstance.DoesNotExist:
            return JsonResponse({'error': 'Instance not found.'}, status=404)
        Payment.objects.create(
            user=request.user,
            amount=amount,
            ghost_instance=ghost_instance,
            paypal_order_id=str(uuid.uuid4())
        )
        return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
    except Exception as e:
        logger.exception("Error processing payment")
        return JsonResponse({'error': 'Payment processing error.'}, status=500)

@login_required
def dashboard(request):
    try:
        instances = GhostInstance.objects.filter(user=request.user)
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'dashboard.html', {'instances': instances, 'payments': payments})
    except Exception as e:
        logger.exception("Dashboard error")
        return JsonResponse({'error': 'Dashboard error.'}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def delete_instance(request, instance_id):
    try:
        instance = GhostInstance.objects.get(id=instance_id, user=request.user)
        if instance.container_id:
            instance_manager.delete_instance(instance.container_id)
        instance.delete()
        return JsonResponse({'message': 'Instance deleted.'})
    except Exception as e:
        logger.exception("Error deleting instance")
        return JsonResponse({'error': 'Instance deletion error.'}, status=500)

@ajax_login_required
def check_instance_status(request, instance_id):
    try:
        instance = GhostInstance.objects.get(id=instance_id, user=request.user)
        status = instance_manager.check_instance_status(instance.container_id) if instance.container_id else 'unknown'
        is_healthy = instance_manager.check_instance_health(instance.port)
        instance.status = 'running' if is_healthy else 'error'
        instance.save()
        return JsonResponse({
            'status': instance.status,
            'is_healthy': is_healthy,
            'last_checked': instance.last_checked
        })
    except Exception as e:
        logger.exception("Error checking status")
        return JsonResponse({'error': 'Status check error.'}, status=500)