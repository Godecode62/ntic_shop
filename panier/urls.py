from django.urls import path
from . import views

urlpatterns = [
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
]
