
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from commande.forms import CommandeForm
from panier.models import Panier, ArticlePanier
from .models import Commande, ArticleCommande
from boutique.models import Produit

@login_required
@login_required
def creer_commande(request):
    try:
        panier = request.user.panier
    except Panier.DoesNotExist:
        messages.error(request, "Votre panier n'existe pas ou a été supprimé.")
        return redirect(reverse('liste_produits'))

    if not panier.items.exists():
        messages.warning(request, "Votre panier est vide. Veuillez ajouter des produits avant de commander.")
        return redirect(reverse('voir_panier'))

    if request.method == 'POST':
        form = CommandeForm(request.POST, user=request.user) # Passe request.POST et l'utilisateur
        if form.is_valid():
            # Les données sont valides, on les récupère
            cleaned_data = form.cleaned_data
            nom = cleaned_data['nom']
            prenom = cleaned_data['prenom']
            email = cleaned_data['email']
            adresse = cleaned_data['adresse']
            code_postal = cleaned_data['code_postal']
            ville = cleaned_data['ville']

            with transaction.atomic():
                try:
                    # 1. Crée la commande
                    commande = Commande.objects.create(
                        user=request.user,
                        nom=nom,
                        prenom=prenom,
                        email=email,
                        adresse=adresse,
                        code_postal=code_postal,
                        ville=ville,
                        statut='pending',
                        payee=False
                    )

                    # 2. Transfère les articles du panier vers la commande et décrémente le stock
                    articles_panier_a_traiter = list(panier.items.all()) # Copie pour éviter les problèmes d'itération

                    for article_panier in articles_panier_a_traiter:
                        produit = article_panier.produit
                        quantite_commandee = article_panier.quantite

                        if produit.stock < quantite_commandee:
                            raise ValueError(f"Stock insuffisant pour '{produit.nom}'. Disponible: {produit.stock}, Demandé: {quantite_commandee}.")

                        ArticleCommande.objects.create(
                            commande=commande,
                            produit=produit,
                            prix=produit.prix,
                            quantite=quantite_commandee
                        )
                        produit.stock -= quantite_commandee
                        produit.save()
                        
                        article_panier.delete()

                    messages.success(request, f"Votre commande #{commande.id} a été passée avec succès !")
                    return redirect(reverse('commande_succes', args=[commande.id]))

                except ValueError as e:
                    messages.error(request, str(e))
                    return redirect(reverse('voir_panier'))
                except Exception as e:
                    messages.error(request, "Une erreur inattendue est survenue lors de la création de votre commande.")
                    return redirect(reverse('voir_panier'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{form[field].label}': {error}")
            return redirect(reverse('voir_panier')) # On redirige pour l'instant
    else:
        # Pour une requête GET, crée une instance vide du formulaire
        form = CommandeForm(user=request.user) # Passe l'utilisateur au formulaire pour pré-remplir

    # Rend le template avec le formulaire et les infos du panier
    return render(request, 'commande/creer_commande.html', {'form': form, 'panier': panier})


# --- Vue : Page de confirmation de commande ---
@login_required
def commande_succes(request, commande_id):
    # Récupère la commande pour l'afficher sur la page de confirmation
    commande = Commande.objects.get(id=commande_id, user=request.user)
    return render(request, 'commande/commande_succes.html', {'commande': commande})


@login_required
def historique_commandes(request):
    # Récupère toutes les commandes de l'utilisateur connecté
    commandes = request.user.commandes.all().order_by('-created_at')
    return render(request, 'commande/historique_commandes.html', {'commandes': commandes})


#Vu pour permettre l'annulation de la commande
@login_required
def annuler_commande(request, commande_id):
    try:
        commande = Commande.objects.get(id=commande_id, user=request.user, statut='pending')
    except Commande.DoesNotExist:
        messages.error(request, "Impossible d'annuler cette commande ou la commande n'est pas annulable à ce stade.")
        return redirect(reverse('historique_commandes'))

    if request.method == 'POST':
        with transaction.atomic():
            try:
                commande.statut = 'cancelled'
                commande.save()

                for article_commande in commande.items.all():
                    produit = article_commande.produit
                    produit.stock += article_commande.quantite
                    produit.save()
                
                messages.success(request, f"La commande #{commande.id} a été annulée avec succès.")
                return redirect(reverse('historique_commandes'))
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'annulation de la commande #{commande.id}.")
                return redirect(reverse('historique_commandes'))
    
    messages.error(request, "Méthode non autorisée pour cette action.")
    return redirect(reverse('historique_commandes'))


#Pour la gestion des commandes par l'administrateur
@login_required
@user_passes_test(lambda u: u.is_staff) # Seuls les utilisateurs staff (admin) peuvent accéder
def gestion_commandes_admin(request):
    commandes = Commande.objects.all().order_by('-created_at') # Récupère TOUTES les commandes

    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        action = request.POST.get('action')
        statut = request.POST.get('statut') # Pour changer le statut
        payee = request.POST.get('payee') # Pour changer le statut de paiement

        commande = get_object_or_404(Commande, id=commande_id)

        with transaction.atomic():
            try:
                if action == 'annuler':
                    if commande.statut != 'cancelled':
                        commande.statut = 'cancelled'
                        commande.save()
                        # Réintégration du stock
                        for article_commande in commande.items.all():
                            produit = article_commande.produit
                            produit.stock += article_commande.quantite
                            produit.save()
                        messages.success(request, f"Commande #{commande.id} annulée et stock réintégré.")
                    else:
                        messages.info(request, f"Commande #{commande.id} est déjà annulée.")
                elif action == 'modifier_statut' and statut:
                    # Assure que le statut est valide avant de l'appliquer
                    if statut in [choice[0] for choice in Commande.STATUT_CHOICES]:
                        commande.statut = statut
                        commande.save()
                        messages.success(request, f"Statut de la commande #{commande.id} mis à jour : {commande.get_statut_display}.")
                    else:
                        messages.error(request, "Statut invalide fourni.")
                elif action == 'modifier_payee':
                    # Convertir 'true'/'false' en booléen
                    commande.payee = (payee == 'true')
                    commande.save()
                    messages.success(request, f"Statut de paiement de la commande #{commande.id} mis à jour : {'Payée' if commande.payee else 'Non payée'}.")
                else:
                    messages.error(request, "Action non reconnue.")

            except Exception as e:
                messages.error(request, f"Erreur lors du traitement de la commande #{commande.id} : {e}")
                # En production, tu logguerais l'erreur ici.
                # import logging
                # logging.exception(f"Erreur admin commande {commande_id}")

        return redirect(reverse('gestion_commandes_admin')) # Recharge la page après action

    # Pour les requêtes GET (affichage initial)
    return render(request, 'commande/gestion_commandes_admin.html', {'commandes': commandes})

