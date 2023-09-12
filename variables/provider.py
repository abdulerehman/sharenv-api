from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
import os

User = get_user_model()


def sign_with_google(token):
    try:
        user_info = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))

        password = user_info["sub"]
        last_name = user_info["given_name"]
        first_name = user_info["family_name"]
        email = user_info["email"]

        user_exist = User.objects.filter(email=email)
        if user_exist.exists():
            return user_exist.get().token()

        user = User.objects.create_user(
            username=email.split("@")[0],
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
            is_active=True,
        )

        return user.token()

    except Exception as e:
        print(e)
        return False
