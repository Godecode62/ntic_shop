from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Importe les modèles de l'application 'boutique'
from boutique.models import Produit
# Importe les modèles de l'application 'panier'
from .models import Panier, ArticlePanier


# --- Fonction utilitaire : Récupérer le panier de l'utilisateur connecté ---
@login_required # S'assure que seul un utilisateur connecté peut appeler cette fonction
def _get_or_create_cart(request):
    """Récupère ou crée le panier d'achat de l'utilisateur."""
    # Django crée ou récupère le panier associé à l'utilisateur actuel.
    panier, created = Panier.objects.get_or_create(user=request.user)
    return panier


# --- Vue : Afficher le contenu du panier ---
@login_required # Un utilisateur doit être connecté pour voir son panier
def voir_panier(request):
    """Affiche la page du panier de l'utilisateur."""
    panier = _get_or_create_cart(request) # On récupère le panier de l'utilisateur
    return render(request, 'panier/voir_panier.html', {'panier': panier})


# --- Vue : Ajouter un produit au panier ---
@require_POST # Accepte uniquement les requêtes envoyées par un formulaire POST
@login_required # Seuls les utilisateurs connectés peuvent ajouter des produits
def ajouter_au_panier(request, produit_id):
    """Ajoute un produit au panier ou augmente sa quantité."""
    produit = get_object_or_404(Produit, id=produit_id) # Vérifie si le produit existe

    try:
        quantite = int(request.POST.get('quantite', 1))
    except (ValueError, TypeError):
        quantite = 1 # Quantité par défaut si l'entrée est invalide

    if quantite <= 0:
        return redirect(reverse('voir_panier')) # Empêche l'ajout de quantités nulles ou négatives

    panier = _get_or_create_cart(request) # Récupère le panier de l'utilisateur

    with transaction.atomic(): # Assure que l'opération est atomique (tout ou rien)
        # Tente de récupérer l'article si déjà dans le panier, sinon le crée
        article_panier, created = ArticlePanier.objects.get_or_create(
            panier=panier,
            produit=produit,
            defaults={'quantite': quantite} # Quantité initiale si l'article est nouveau
        )
        if not created:
            # Si l'article existait déjà, on incrémente la quantité et on sauvegarde
            article_panier.quantite += quantite
            article_panier.save()

    return redirect(reverse('voir_panier')) # Redirige l'utilisateur vers la page du panier


# --- Vue : Retirer un article du panier ---
@require_POST # Accepte uniquement les requêtes POST (via formulaire)
@login_required # Seuls les utilisateurs connectés peuvent retirer des produits
def retirer_du_panier(request, article_id):
    """Retire un article spécifique du panier de l'utilisateur."""
    panier = _get_or_create_cart(request) # Récupère le panier de l'utilisateur
    # Vérifie que l'article existe ET qu'il appartient bien au panier de l'utilisateur
    article_panier = get_object_or_404(ArticlePanier, id=article_id, panier=panier)
    
    article_panier.delete() # Supprime l'article du panier
    
    return redirect(reverse('voir_panier')) # Redirige vers la page du panier


# --- Vue : Mettre à jour la quantité d'un article dans le panier ---
@require_POST # Accepte uniquement les requêtes POST (via formulaire)
@login_required # Seuls les utilisateurs connectés peuvent modifier leur panier
def maj_quantite_panier(request, article_id):
    """Met à jour la quantité d'un article existant dans le panier."""
    panier = _get_or_create_cart(request) # Récupère le panier de l'utilisateur
    # Vérifie que l'article existe ET qu'il appartient bien au panier de l'utilisateur
    article_panier = get_object_or_404(ArticlePanier, id=article_id, panier=panier)
    
    try:
        nouvelle_quantite = int(request.POST.get('quantite', 1))
    except (ValueError, TypeError):
        nouvelle_quantite = 1 # Quantité par défaut si l'entrée est invalide

    with transaction.atomic(): # Assure que l'opération est atomique
        if nouvelle_quantite <= 0:
            article_panier.delete() # Supprime l'article si la quantité est zéro ou moins
        else:
            article_panier.quantite = nouvelle_quantite # Met à jour la quantité
            article_panier.save() # Sauvegarde la modification

    return redirect(reverse('voir_panier')) # Redirige vers la page du panier