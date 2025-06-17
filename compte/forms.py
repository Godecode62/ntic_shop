
from django import forms
from .models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}),
        label="Confirmer le mot de passe"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password') 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone (ex: +224 620 00 00 00)'}),
        }
        labels = {
            'username': "Nom d'utilisateur",
            'email': "Adresse email",
            'phone_number': "Numéro de téléphone",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        # Ajout des widgets pour les classes Bootstrap et placeholders
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom de famille'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre adresse email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: +224 620 00 00 00'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifie si l'email existe déjà pour un autre utilisateur, sauf l'utilisateur actuel
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée par un autre compte.")
        return email



#Pour le changement de mot de passe
class CustomPasswordChangeForm(PasswordChangeForm):
    # Redéfinir les champs pour les libellés et les widgets en français
    old_password = forms.CharField(
        label="Ancien mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre ancien mot de passe'})
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nouveau mot de passe'}),
        help_text="Votre mot de passe doit contenir au moins 8 caractères."
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre nouveau mot de passe'})
    )

    class Meta:
        model = None # PasswordChangeForm ne se lie pas directement à un modèle
        fields = ['old_password', 'new_password1', 'new_password2']