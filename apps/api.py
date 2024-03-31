from fastapi import APIRouter
from apps.user.routers import user_router
from apps.auth.jwt import auth_router
from apps.image.routers import img_router
from apps.feature.routers import feat_router
from apps.auto.routers import auto_router
from apps.profile.routers import profile_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(img_router, prefix="/img", tags=["image"])
router.include_router(feat_router, prefix="/feat", tags=["feature"])
router.include_router(auto_router, prefix="/auto", tags=["auto"])
router.include_router(profile_router, prefix="/profile", tags=["profile"])