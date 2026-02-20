# -*- coding: utf-8 -*-
"""
Пользовательские формы для приложения bodies
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SimplifiedUserCreationForm(forms.ModelForm):
    """
    Упрощённая форма регистрации с более мягкими требованиями к паролю
    """
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        min_length=4,
        help_text="Минимум 4 символа"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        min_length=4,
        help_text="Введите пароль ещё раз"
    )
    
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Выберите имя пользователя'}),
        help_text="Только буквы, цифры и @/./+/-/_"
    )
    
    class Meta:
        model = User
        fields = ('username',)
    
    def clean_username(self):
        """Проверка уникальности имени пользователя"""
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError("Имя пользователя не может быть пустым")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Пользователь с именем '{username}' уже существует")
        
        return username
    
    def clean(self):
        """Проверка паролей и совпадение"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают!")
        
        return cleaned_data
    
    def save(self, commit=True):
        """Сохранение пользователя с паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

