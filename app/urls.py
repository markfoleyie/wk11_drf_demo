from django.urls import path

from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/', views.Register.as_view(), name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='login_user'),
    path('user/me/', views.UserMeDetails.as_view(), name='get_current_user_details'),
]