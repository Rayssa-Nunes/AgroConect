from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Usuário', 'required': True})
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'E-mail', 'required': True})
        self.fields['email'].label = ''

        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha', 'required': True})
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar senha', 'required': True})
        self.fields['password2'].label = ''


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'E-mail'})
        self.fields['username'].label = ''
        
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password'].label = ''


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Endereço de email'})
        self.fields['email'].label = ''

from django.utils.safestring import mark_safe
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua nova senha',
            'autocomplete': 'new-password',
        }),
        strip=False,
        help_text=mark_safe(
            '''
            <ul>
                <li>Sua senha não pode ser muito parecida com o resto das suas informações pessoais.</li>
                <li>Sua senha precisa conter pelo menos 8 caracteres.</li>
                <li>Sua senha não pode ser uma senha comumente utilizada.</li>
                <li>Sua senha não pode ser inteiramente numérica.</li>
            </ul>
            '''
        )
    )
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua nova senha',
            'autocomplete': 'new-password',
        }),
        help_text=mark_safe(
            '<span>Informe a mesma senha informada anteriormente, para verificação.</span>'
        )
    )