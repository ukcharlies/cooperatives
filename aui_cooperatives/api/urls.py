from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
    path("user/", get_user),
    path("news/", get_news_events),
]
