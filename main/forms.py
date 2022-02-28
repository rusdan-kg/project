from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django import forms
from main.models import Product, ConfirmCode
from django.contrib.auth.models import User
from django.conf import settings
import secrets

class RegisterForm(forms.Form):
    username = forms.CharField(label='Пользователь', min_length=3, max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Ваш логин'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите электронную почту'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите секретный ключ'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите секретный ключ'
    }))
    def clean_username(self):
        username =self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if users.count() > 0:
            raise ValidationError('Такое имя уже существует')
        return username
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('Пароли не совпадают')
        return password

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            is_active=False
        )
        code = secrets.token_hex(10)
        ConfirmCode.objects.create(user=user, code=code)
        send_mail(
            subject='Test subject',
            message='',
            html_message=f'<a href="http://localhost:8000/confirm/?code={code}">Confirm please</a>',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.cleaned_data['email']],
            fail_silently=False
        )
        return user

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'   #выборка вывода по всем категориям
        fields = ['title', 'category', 'price', 'description', 'date_end', 'size']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название', 'class': 'form-control'}),
            'category': forms.Select(attrs={'placeholder': 'Выберите категорию', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Введите цену', 'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'placeholder': 'Введите срок годности', 'class': 'form-control'}),
            'size': forms.TextInput(attrs={'placeholder': 'Введите объем', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Введите описание', 'class': 'form-control'}),
        }
