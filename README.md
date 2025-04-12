# Twilio Order Agent

A Django-based automated ordering system that uses Twilio for processing customer orders via SMS and voice calls.

## Overview

This system allows customers to place orders through text messages or phone calls. It uses natural language processing to recognize customer intents and automatically processes orders, providing real-time confirmations and status updates.

![System Architecture](https://raw.githubusercontent.com/pkalosh/E-commerce-order-processing-agent-twilio/main/docs/system-architecture.png)

## Features

- **Multi-channel Communication**: Process orders via SMS text messages and voice calls
- **Intent Recognition**: Automatically recognize customer intents (place orders, check status)
- **Automated Order Processing**: Handle the complete order lifecycle
- **Real-time Confirmations**: Send order confirmations and status updates
- **Admin Dashboard**: Monitor and manage orders through Django admin

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Communication**: Twilio API (SMS and Voice)
- **Development Tools**: ngrok (for local webhook testing)

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Twilio account
- ngrok account (for local development)

### Setup

1. Clone the repository
```bash
git clone https://github.com/pkalosh/E-commerce-order-processing-agent-twilio.git
cd E-commerce-order-processing-agent-twilio
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your Twilio credentials
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser for the admin interface
```bash
python manage.py createsuperuser
```

6. Start the development server
```bash
python manage.py runserver
```

## Twilio Configuration

1. Set up a Twilio account and obtain a phone number
2. Configure webhook URLs for your Twilio phone number:
   - For SMS: `https://your-domain.com/twilio/sms-webhook/`
   - For Voice: `https://your-domain.com/twilio/voice-webhook/`

## Local Development with ngrok

For local testing, use ngrok to create a secure tunnel to your local server:

```bash
ngrok http 8000
```

Update your Twilio webhook URLs with the ngrok URL.

## Usage

### Testing with cURL

You can test the SMS webhook locally using cURL:

```bash
curl -X POST http://localhost:8000/twilio/sms-webhook/ \
  -d "From=+15555555555" \
  -d "Body=I'd like to order 2 pizzas"
```

### Sample Customer Interactions

- **Text to order**: "I want to order 2 large pizzas and a soda"
- **Check order status**: "What's the status of my order?"

## Project Structure

```
agentic_order_system/
├── core/                # Core application
│   ├── models.py        # Database models
│   ├── intent_recognition.py  # Intent processing
├── twilio_integration/  # Twilio webhook handling
│   ├── views.py         # Webhook endpoints
│   ├── urls.py          # URL routing
├── manage.py            # Django management script
└── requirements.txt     # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.