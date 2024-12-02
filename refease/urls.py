# refease/urls.py

from django.contrib import admin
from django.urls import path, include
from referral_app import views as referral_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', referral_views.home, name='home'),
    path('phone/', referral_views.phone_view, name='phone'),
    path('code/', referral_views.code_view, name='code'),
    path('profile/', referral_views.profile_view, name='profile'),
    path('activate/', referral_views.activate_invite_view, name='activate_invite'),
    path('api/', include('referral_app.urls')),
]
