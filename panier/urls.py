# panier/urls.py

from django.urls import path
from . import views # On importe toutes les fonctions de vue de ton fichier views.py

urlpatterns = [
    # URL pour afficher le contenu du panier
    # Ex: /panier/
    path('panier', views.voir_panier, name='voir_panier'),

    # URL pour ajouter un produit au panier
    # Ex: /panier/ajouter/5/ (où 5 est l'ID du produit)
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),

    # URL pour retirer un article du panier
    # Ex: /panier/retirer/123/ (où 123 est l'ID de l'ArticlePanier)
    path('retirer/<int:article_id>/', views.retirer_du_panier, name='retirer_du_panier'),

    # URL pour mettre à jour la quantité d'un article dans le panier
    # Ex: /panier/maj_quantite/123/ (où 123 est l'ID de l'ArticlePanier)
    path('maj_quantite/<int:article_id>/', views.maj_quantite_panier, name='maj_quantite_panier'),
]