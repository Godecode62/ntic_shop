# commande/forms.py

from django import forms

class CommandeForm(forms.Form):
    # Champs pour les informations de livraison/facturation
    nom = forms.CharField(max_length=100, required=True, label='Nom')
    prenom = forms.CharField(max_length=100, required=True, label='Prénom')
    email = forms.EmailField(required=True, label='Email')
    adresse = forms.CharField(max_length=250, required=True, label='Adresse')
    code_postal = forms.CharField(max_length=20, required=True, label='Code Postal')
    ville = forms.CharField(max_length=100, required=True, label='Ville')
    phone_number = forms.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        # Permet de passer l'utilisateur (si disponible) au formulaire pour pré-remplir les champs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pré-remplir les champs avec les données de l'utilisateur s'il est connecté
        if self.user and self.user.is_authenticated:
            self.fields['nom'].initial = self.user.first_name
            self.fields['prenom'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = self.user.phone_number
