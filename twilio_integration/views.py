from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from django.conf import settings
from core.models import Customer, Order
from core.intent_recognition import IntentRecognizer

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
intent_recognizer = IntentRecognizer()

@csrf_exempt
def sms_webhook(request):
    """Handle incoming SMS messages from Twilio"""
    incoming_message = request.POST.get('Body', '')
    from_number = request.POST.get('From', '')
    print(incoming_message, from_number)
    # Get or create customer
    customer, created = Customer.objects.get_or_create(
        phone_number=from_number,
        defaults={'name': 'Customer'}
    )
    
    # Recognize intent
    intent = intent_recognizer.recognize_intent(incoming_message)
    
    # Process based on intent
    response_message = process_intent(intent, incoming_message, customer)
    
    # Create Twilio response
    resp = MessagingResponse()
    resp.message(response_message)
    
    return HttpResponse(str(resp))

def process_intent(intent, message, customer):
    """Process message based on recognized intent"""
    if intent == "place_order":
        # Extract order details
        order_details = intent_recognizer.extract_order_details(message, intent)
        
        # Create order
        if order_details.get('items'):
            order = Order.objects.create(
                customer=customer,
                order_details=order_details,
                status='pending'
            )
            # Process order (in production, this might be a background task)
            process_order(order)
            return f"Thank you! Your order #{order.id} has been received and is being processed."
        else:
            return "I couldn't understand your order. Please provide product and quantity details."
    
    elif intent == "order_status":
        # Get latest order for the customer
        latest_order = Order.objects.filter(customer=customer).order_by('-created_at').first()
        if latest_order:
            return f"Your order #{latest_order.id} is currently {latest_order.status}."
        else:
            return "You don't have any recent orders."
    
    else:
        return "I'm not sure what you're asking for. You can place an order or check your order status."

def process_order(order):
    """Process the order"""
    # In a real system, this would include payment processing, inventory checks, etc.
    order.status = 'processing'
    order.save()
    
    # Send confirmation to customer
    send_order_confirmation(order)
    
    # Update order status to completed
    order.status = 'completed'
    order.save()

def send_order_confirmation(order):
    """Send order confirmation to customer"""
    message = client.messages.create(
        body=f"Your order #{order.id} has been processed successfully!",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=order.customer.phone_number
    )
    return message.sid



@csrf_exempt
def voice_webhook(request):
    """Handle incoming voice calls from Twilio"""
    response = VoiceResponse()
    
    gather = Gather(input='speech', action='/twilio/voice-intent/', method='POST')
    gather.say('Welcome to our ordering system. How can I help you today?')
    response.append(gather)
    
    # If customer doesn't say anything
    response.say('I didn\'t hear anything. Please call back when you\'re ready.')
    
    return HttpResponse(str(response), content_type='text/xml')

@csrf_exempt
def voice_intent(request):
    """Process speech from voice call"""
    speech_result = request.POST.get('SpeechResult', '')
    from_number = request.POST.get('From', '')
    
    # Get or create customer
    customer, created = Customer.objects.get_or_create(
        phone_number=from_number,
        defaults={'name': 'Customer'}
    )
    
    # Recognize intent
    intent = intent_recognizer.recognize_intent(speech_result)
    
    # Process intent
    response_message = process_intent(intent, speech_result, customer)
    
    # Create Twilio response
    response = VoiceResponse()
    response.say(response_message)
    
    return HttpResponse(str(response), content_type='text/xml')