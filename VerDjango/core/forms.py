from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .validators import *

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'user_type', 'password1', 'password2', 'avatar']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("El correo electrónico contiene caracteres inválidos.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        if " " in password1:
            raise ValidationError("La contraseña no debe contener espacios.")
        if not any(char.isdigit() for char in password1):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not any(char.islower() for char in password1):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not any(char.isupper() for char in password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("El nombre solo debe contener letras.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("El apellido solo debe contener letras.")
        return last_name


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nombre', 'direccion', 'latitud', 'longitud', 'categoria', 'telefono', 'whatsapp', 'correo', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = [ 'descripcion', 'categoria', 'prioridad', 'captura', 'contacto' ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'captura': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }