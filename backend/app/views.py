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

# Set your secret key. Remember to switch to your live secret key in production!

# Configure logging
logger = logging.getLogger(__name__)

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
            
            # Find an available port (starting from 2369)
            used_ports = GhostInstance.objects.values_list('port', flat=True)
            port = 2369
            while port in used_ports:
                port += 1

            # Create Ghost instance in database
            ghost_instance = GhostInstance.objects.create(
                name=instance_name,
                user=request.user,
                port=port
            )

            # Create Docker container for Ghost instance
            client = docker.from_env()
            container = client.containers.run(
                'ghost:latest',
                name=f'ghost_{instance_name}',
                ports={2368: port},
                environment={
                    'url': f'http://localhost:{port}'
                },
                detach=True
            )

            return JsonResponse({
                'message': 'Ghost instance rented successfully!',
                'instance_url': f'http://localhost:{port}'
            })
        except Exception as e:
            logger.error(f"Error renting Ghost instance: {e}")
            return JsonResponse({'error': 'Error renting Ghost instance.'}, status=500)
    else:
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