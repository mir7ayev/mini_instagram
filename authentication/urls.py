from django.urls import path
from .views import (
    signup_view, signin_view, logout_view,
)

urlpatterns = [
    path('signup/', signup_view),
    path('signin/', signin_view),
    path('logout/', logout_view)
]
