from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from .models import User


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_staff', 'is_superuser']


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password')

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']

    def clean_password(self):
        return self.initial['password']
