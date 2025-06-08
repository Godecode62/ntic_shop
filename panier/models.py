
from django.db import models
from django.conf import settings

# Importe le modèle Produit de ton application 'boutique'
from boutique.models import Produit

class Panier(models.Model):
    """
    Représente le panier d'achat, STRICTEMENT lié à un utilisateur connecté.
    """
    # Un panier est lié à un utilisateur. Si l'utilisateur est supprimé, son panier l'est aussi.
    # related_name='panier' est ici un OneToOneField, donc user.panier accédera directement au panier.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='panier'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    @property
    def get_total_price(self):
        """
        Calcule le prix total de tous les articles dans le panier.
        """
        total = sum(item.get_total for item in self.items.all())
        return total

    @property
    def get_total_items(self):
        """
        Calcule le nombre total d'articles (quantité cumulée) dans le panier.
        """
        total = sum(item.quantite for item in self.items.all())
        return total


class ArticlePanier(models.Model):
    """
    Représente un produit spécifique dans un panier, avec sa quantité.
    """
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('panier', 'produit')
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    @property
    def get_total(self):
        return self.quantite * self.produit.prix