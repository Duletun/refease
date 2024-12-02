from django import forms

class PhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label='Номер телефона')

class CodeForm(forms.Form):
    code = forms.CharField(max_length=4, label='Код авторизации')

class ActivateInviteForm(forms.Form):
    invite_code = forms.CharField(max_length=6, label='Инвайт-код')
