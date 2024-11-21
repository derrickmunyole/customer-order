# Forever Locket App

## Project Overview: OAuth-Powered Django App with SMS Notifications
The **Forever Locket App** is a demonstration of integrating third-party authentication and real-time user notifications in a Django web application. It showcases how a full-stack solution can be architected using modern tools like Docker, OAuth, and Django signals.

This app is designed to be a starting point for developers looking to build secure, notification-driven web applications. It's perfect for e-commerce platforms, event management tools, or any project needing order tracking with real-time updates.

## Key Features

- **OAuth Authentication**: Secure user login using Google's OAuth, providing a user-friendly and secure way to access the app.
- **Robust Backend**: Powered by Django, offering seamless request processing and database interactions.
- **Persistent Data Storage**: Utilizes PostgreSQL for reliable storage of user data and order records.
- **Dockerized Environment**: Streamlined development and deployment with Docker and Docker Compose.
- **Item Listing and Order Simulation**: Users can browse and place orders for pre-defined items.
- **Django Signals & SMS Notifications**: Automatic SMS notifications for each order, sent via Africa's Talking API.

## Tech Stack
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker
- **OAuth Provider**: Google OAuth 2.0
- **Notification Service**: Africa's Talking API
- **Configuration Management**: Pulumi/Ansible (deployment)

## Installation and Setup
To set up the project locally, follow these steps:
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd customer-order

 2. cp .env.example .env

 3. docker-compose up --build

 4. Access the app at http://localhost:8000

 # Usage

**User Authentication**: Press the sign in button to sign using your Google account.
**Place Orders**: Browse the item listings and place an order.
**Receive SMS Alerts**: Upon order placement, an SMS confirmation will be sent.View the sms notification on the AfricasTalking emulator in the  developer docs


# Configuration and Environment Variables

The project uses the following environment variables:
**GOOGLE_CLIENT_ID**: Your Google OAuth client ID.  
**GOOGLE_CLIENT_SECRET**: Your Google OAuth client secret.  
**AFRICASTALKING_API_KEY**: API key for sending SMS notifications.  
**POSTGRES_DB**: PostgreSQL database name.  
**POSTGRES_USER**: Database username.  
**POSTGRES_PASSWORD**: Database password.  
**DJANGO_SECRET_KEY** Django Secret Key  

## Known Issues and Limitations
**Functional Tests**: Currently incomplete; only unit and integration tests are included.  
**Deployment Limitations**: Initial deployment using Pulumi/Ansible may need further testing.