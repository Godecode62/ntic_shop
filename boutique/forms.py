from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    nom = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Donner un nom pour ce produit',
            'class': 'form-control'
        })
    )

    description = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Décrire brièvement le produit',
            'rows': 4,
            'class': 'form-control'
        })
    )

    prix = forms.DecimalField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Donner un prix pour ce produit',
            'class': 'form-control'
        })
    )

    stock = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Quantité en stock',
            'class': 'form-control'
        })
    )

    disponible = forms.BooleanField(
        label='Disponible',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    image = forms.ImageField(
        label='Image (facultative)',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    categorie = forms.ModelChoiceField(
        queryset=None,
        label='',
        empty_label='Choisir une catégorie',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'stock', 'disponible', 'image', 'categorie']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].queryset = Produit._meta.get_field('categorie').related_model.objects.all()
