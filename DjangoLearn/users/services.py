import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed
from DjangoLearn.users.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

User = get_user_model()


def register_user(data: dict) -> dict:
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    tokens = generate_tokens(user)
    logger.info("New user registered: %s", user.email)
    return tokens


def login_user(email: str, password: str) -> dict:
    user = authenticate(email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Invalid email or password")

    tokens = generate_tokens(user)
    logger.info("User logged in: %s", user.email)
    return tokens


def generate_tokens(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def logout_user(refresh_token: str) -> None:
    token = RefreshToken(refresh_token)
    token.blacklist()
    logger.info("User logged out")
