# backend/app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
import stripe
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth.decorators import login_required
from .models import GhostInstance, Payment  # These are the correct models
import docker
from .utils import InstanceManager
from django.conf import settings

# Set your secret key. Remember to switch to your live secret key in production!

# Configure logging
logger = logging.getLogger(__name__)

instance_manager = InstanceManager()

def home(request):
    try:
        response = render(request, 'index.html')
        response.set_cookie('csrftoken', get_token(request))
        return response
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return JsonResponse({'error': 'Error rendering home page.'}, status=500)

def contact(request):
    try:
        return render(request, 'contact.html')
    except Exception as e:
        logger.error(f"Error rendering contact page: {e}")
        return JsonResponse({'error': 'Error rendering contact page.'}, status=500)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            YOUR_DOMAIN = "http://localhost:8000"  # Replace with your actual domain
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Your Product Name',  # Replace with your product name
                            },
                            'unit_amount': 2000,  # Replace with your product price in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return JsonResponse({'id': checkout_session.id})
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            return JsonResponse({'error': 'Stripe error occurred.'}, status=500)
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            return JsonResponse({'error': 'Error creating checkout session.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def success(request):
    try:
        return render(request, 'success.html')
    except Exception as e:
        logger.error(f"Error rendering success page: {e}")
        return JsonResponse({'error': 'Error rendering success page.'}, status=500)

def cancel(request):
    try:
        return render(request, 'cancel.html')
    except Exception as e:
        logger.error(f"Error rendering cancel page: {e}")
        return JsonResponse({'error': 'Error rendering cancel page.'}, status=500)

@csrf_exempt
@login_required
def rent_ghost(request):
    if request.method == 'POST':
        try:
            instance_name = request.POST.get('instance_name')
            
            # Find available port
            used_ports = GhostInstance.objects.values_list('port', flat=True)
            port = settings.GHOST_BASE_PORT + 1
            while port in used_ports:
                port += 1

            # Create Ghost instance in database
            ghost_instance = GhostInstance.objects.create(
                name=instance_name,
                user=request.user,
                port=port,
                status='creating'
            )

            try:
                # Create Docker container
                container_id = instance_manager.create_instance(instance_name, port)
                ghost_instance.container_id = container_id
                ghost_instance.status = 'running'
                ghost_instance.save()

                return JsonResponse({
                    'message': 'Ghost instance created successfully!',
                    'instance_id': ghost_instance.id,
                    'instance_url': ghost_instance.get_url()
                })
            except Exception as e:
                ghost_instance.status = 'error'
                ghost_instance.error_message = str(e)
                ghost_instance.save()
                raise

        except Exception as e:
            logger.error(f"Error renting Ghost instance: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
@login_required
def process_payment(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            instance_id = request.POST.get('instance_id')
            ghost_instance = GhostInstance.objects.get(id=instance_id)

            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'ghost_instance_id': instance_id
                }
            )

            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                stripe_payment_id=intent.id,
                ghost_instance=ghost_instance
            )

            return JsonResponse({
                'client_secret': intent.client_secret,
                'message': 'Payment processed successfully!'
            })
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return JsonResponse({'error': 'Error processing payment.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def dashboard(request):
    try:
        instances = GhostInstance.objects.filter(user=request.user)
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'dashboard.html', {
            'instances': instances,
            'payments': payments
        })
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return JsonResponse({'error': 'Error loading dashboard.'}, status=500)

@csrf_exempt
@login_required
def delete_instance(request, instance_id):
    if request.method == 'POST':
        try:
            instance = GhostInstance.objects.get(id=instance_id, user=request.user)
            if instance.container_id:
                instance_manager.delete_instance(instance.container_id)
            instance.delete()
            return JsonResponse({'message': 'Instance deleted successfully'})
        except Exception as e:
            logger.error(f"Error deleting instance: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def check_instance_status(request, instance_id):
    try:
        instance = GhostInstance.objects.get(id=instance_id, user=request.user)
        if instance.container_id:
            status = instance_manager.check_instance_status(instance.container_id)
            is_healthy = instance_manager.check_instance_health(instance.port)
            
            instance.status = 'running' if is_healthy else 'error'
            instance.save()
            
            return JsonResponse({
                'status': instance.status,
                'is_healthy': is_healthy,
                'last_checked': instance.last_checked
            })
    except Exception as e:
        logger.error(f"Error checking instance status: {e}")
        return JsonResponse({'error': str(e)}, status=500)