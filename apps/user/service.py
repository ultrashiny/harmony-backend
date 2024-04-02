from uuid import UUID

from fastapi import HTTPException, status
from apps.security import get_password, verify_password
from typing import Optional
from .schemas import UserAuth, UserOut, UserSubscription, UserUpdate
from .models import User
import stripe

class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password),
            customer_id=stripe.Customer.create(email = user.email)["id"]
        )
        await user_in.save()
        return user_in
    
    @staticmethod
    async def update_user(user: UserUpdate):
        existing_profile = await User.find_one(User.email == user.email)
        if existing_profile:
            await existing_profile.update(
                {
                    "$set": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "customer_id": user.customer_id,
                        "subscription_id": user.subscription_id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The email never registered.")
    
    @staticmethod
    async def create_subscription(data: UserSubscription):
        try:
            stripe.PaymentMethod.attach(
                data.payment_method_id,
                customer = data.customer_id
            )
            
            stripe.Customer.modify(
                data.customer_id,
                invoice_settings={"default_payment_method": data.payment_method_id}
            )
            
            subscription = stripe.Subscription.create(
                customer=data.customer_id,
                items=[{"price": data.price_id}],
                expand=["latest_invoice.payment_intent"],
            )
            
            user = await UserService.get_user_by_id(data.user_id)
            if user:
                user.subscription_id = subscription.id
                user.credits += 5
                await user.save()
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email = email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None

        return user
                

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user