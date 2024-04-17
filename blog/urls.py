from django.urls import path
from .views import (
    home_view, profile_view, settings_view,
    follow, like,
)

urlpatterns = [
    path('', home_view),
    path('follow/', follow),
    path('like/', like),
    path('profile/', profile_view),
    path('settings/', settings_view),
]
