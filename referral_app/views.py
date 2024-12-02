# referral_app/views.py

from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import User
from .forms import PhoneForm, CodeForm, ActivateInviteForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PhoneSerializer, CodeSerializer, ProfileSerializer, ActivateInviteSerializer

import random
import time

# Классы для API

class PhoneVerificationView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = str(random.randint(1000, 9999))
            cache.set(phone_number, code, timeout=300)
            # Имитация задержки и отправки СМС
            time.sleep(2)
            print(f"Отправлен код {code} на номер {phone_number}")
            return Response({'message': 'Код отправлен'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CodeVerificationView(APIView):
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            cached_code = cache.get(phone_number)
            if cached_code == code:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                return Response({'message': 'Авторизация успешна'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request, phone_number):
        try:
            user = User.objects.get(phone_number=phone_number)
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, phone_number):
        serializer = ActivateInviteSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.activated_invite_code:
                    return Response({'error': 'Инвайт-код уже активирован'}, status=status.HTTP_400_BAD_REQUEST)
                referrer = User.objects.get(invite_code=invite_code)
                user.activated_invite_code = invite_code
                referrer.referrals.add(user)
                user.save()
                referrer.save()
                return Response({'message': 'Инвайт-код успешно активирован'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Неверный инвайт-код или пользователь'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Функции для веб-интерфейса

def home(request):
    return render(request, 'home.html')

def phone_view(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = str(random.randint(1000, 9999))
            cache.set(phone_number, code, timeout=300)
            time.sleep(2)
            request.session['phone_number'] = phone_number
            # В реальном приложении код отправляется по СМС
            print(f"Отправлен код {code} на номер {phone_number}")
            return redirect('code')
    else:
        form = PhoneForm()
    return render(request, 'phone.html', {'form': form})

def code_view(request):
    phone_number = request.session.get('phone_number')
    if not phone_number:
        return redirect('phone')
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            cached_code = cache.get(phone_number)
            if cached_code == code:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                request.session['user_id'] = user.id
                return redirect('profile')
            else:
                form.add_error('code', 'Неверный код')
    else:
        form = CodeForm()
    return render(request, 'code.html', {'form': form})

def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('phone')
    user = User.objects.get(id=user_id)
    referrals = user.referrals.all()
    return render(request, 'profile.html', {'user': user, 'referrals': referrals})

def activate_invite_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('phone')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = ActivateInviteForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']
            if user.activated_invite_code:
                form.add_error('invite_code', 'Вы уже активировали инвайт-код')
            else:
                try:
                    referrer = User.objects.get(invite_code=invite_code)
                    user.activated_invite_code = invite_code
                    referrer.referrals.add(user)
                    user.save()
                    referrer.save()
                    return redirect('profile')
                except User.DoesNotExist:
                    form.add_error('invite_code', 'Неверный инвайт-код')
    else:
        form = ActivateInviteForm()
    return render(request, 'activate_invite.html', {'form': form})
