from django.urls import path
from .views import PhoneVerificationView, CodeVerificationView, ProfileView

urlpatterns = [
    path('auth/phone/', PhoneVerificationView.as_view(), name='phone_verification'),
    path('auth/code/', CodeVerificationView.as_view(), name='code_verification'),
    path('profile/<str:phone_number>/', ProfileView.as_view(), name='profile'),
]
