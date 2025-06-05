from django.shortcuts import redirect, get_object_or_404
from boutique.models import Produit

# ✅ Fonction pour ajouter un produit au panier
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    panier = request.session.get('panier', {})  # récupère ou crée un panier

    # Ajouter le produit au panier (clé = id, valeur = quantité)
    if str(produit_id) in panier:
        panier[str(produit_id)] += 1
    else:
        panier[str(produit_id)] = 1

    request.session['panier'] = panier  # on sauvegarde le panier dans la session
    return redirect('detail_produit', id=produit_id)  # redirection vers la page du produit
