from django import forms
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from .models import ContactRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['full_name', 'email', 'phone', 'description']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'})

        }
class CreateRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['full_name', 'email', 'phone', 'description','status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'})  # Стилизованный выпадающий список
        }

class ContactRequestDeleteView(DeleteView):
    model = ContactRequest
    template_name = 'delete_contact_request.html'  # Имя шаблона для подтверждения удаления
    success_url = reverse_lazy('contact_request_list')  # Перенаправление после успешного удаления
    context_object_name = 'contact_request'  # Имя объекта в контексте



class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['full_name', 'phone', 'email', 'description', 'file', 'status']  # В

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))