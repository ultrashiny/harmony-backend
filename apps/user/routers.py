from fastapi import APIRouter, Depends, HTTPException, Header, Request, status

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
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or email already exists."
        )

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
async def cancel_subscription(subscription_id: str):
    try:
        canceled_subscription = stripe.Subscription.delete(subscription_id)
        return {"status": "success", "data": canceled_subscription}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
# @user_router.post('/webhook')
# async def webhook(request: Request, stripe_signature: str = Header(None)):
#     webhook_secret = os.environ["STRIPE_WEBHOOK_SECRET"]
#     data = await request.body()
#     try:
#         event = stripe.Webhook.construct_event(
#             payload=data,
#             sig_header=stripe_signature,
#             secret=webhook_secret
#         )
#         event_data = event['data']
#     except Exception as e:
#         return {"error": str(e)}

#     event_type = event['type']
#     if event_type == 'checkout.session.completed':
#         print('checkout session completed')
#     elif event_type == 'invoice.paid':
#         print('invoice paid')
#     elif event_type == 'invoice.payment_failed':
#         print('invoice payment failed')
#     else:
#         print(f'unhandled event: {event_type}')
    
#     return {"status": "success"}
    