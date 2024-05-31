from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from fastapi.responses import JSONResponse

from apps.user.deps import get_current_user
from apps.user.models import User
from .schemas import UserAuth, UserOut, UserPayload, UserSubscription, UserUpdate
from .service import UserService
import pymongo
import stripe
import os

from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

user_router = APIRouter()
@user_router.post('/create', summary="Create a new user", response_model=User)
async def create_user(data: UserAuth):
    if not data.username or not data.email or not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username, email, and password are required."
        )
    existing_user = await UserService.get_user_by_email(email=data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
        
    try:
        new_user = await UserService.create_user(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or email already exists."
        )
        
    return new_user

@user_router.post('/update', summary="Update a user")
async def update_user(data: UserUpdate):
    try:
        return await UserService.update_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
        
@user_router.post('/create_subscription')
async def create_subscription(data: UserSubscription):
    try:
        return await UserService.create_subscription(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@user_router.post('/create-checkout-session')
async def create_checkout_session(url: str, price_id: str, user:User = Depends(get_current_user)):
    response = stripe.checkout.Session.create(
        success_url=url,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        customer=user.customer_id,
    )
    return response.url

@user_router.post('/cancel_subscription')
async def cancel_subscription(subscription_id: str, user:User = Depends(get_current_user)):
    try:
        canceled_subscription = stripe.Subscription.delete(subscription_id)
        if user:
            user.auth = 0
            user.subscription_id = None
            await user.save()
        return {"status": "success", "data": canceled_subscription}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@user_router.post('/webhook')
async def webhook(request: Request):
    print("Received Stripe webhook event")
    webhook_secret = os.environ["STRIPE_WEBHOOK_SECRET"]
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        # Invalid payload
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Invalid payload"})
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Invalid signature"})

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        customer_id = invoice['customer']  # Get the customer ID from the invoice object
        customer = stripe.Customer.retrieve(customer_id)  # Retrieve customer information
        user = await UserService.get_user_by_customer_id(customer_id)  # Retrieve user based on customer ID

        # Retrieve subscription and product details as previously
        subscription_id = invoice['subscription']
        subscription = stripe.Subscription.retrieve(subscription_id)
        product_id = subscription['plan']['product']
        product = stripe.Product.retrieve(product_id)
        
        # Check product type and perform actions
        if product['name'].lower() == 'premium':
            user.auth = 1
            user.credit += 5
            user.subscription_id = subscription_id
            print(f"Premium product charge succeeded for customer {customer['email']} or {customer['name']}.")
        elif product['name'].lower() == 'plantium':
            user.auth = 2
            user.credit += 30
            user.subscription_id = subscription_id
            print(f"Plantium product charge succeeded for customer {customer['email']} or {customer['name']}.")
        else:
            print(f"Other product charge succeeded for customer {customer['email']} or {customer['name']}.")

        await user.save()
        # Optionally, you can handle more customer details here
        print(f"Customer Details: Email={customer.get('email', 'Not provided')}, Name={customer.get('name', 'Anonymous')}")

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Received"})
    