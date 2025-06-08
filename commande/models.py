
from django.db import models
from django.conf import settings
from boutique.models import Produit

class Commande(models.Model):
    # L'utilisateur lié à la commande (peut être NULL si compte supprimé)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='commandes')
    
    # Informations de livraison/facturation (copie pour l'historique)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)

    # Statut de la commande
    STATUT_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('shipped', 'Expédiée'),
        ('cancelled', 'Annulée'),
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Indique si la commande a été payée
    payee = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f'Commande {self.id}'

    def get_total_cost(self):
        # Calcule le coût total de la commande
        return sum(item.get_cost() for item in self.items.all())


class ArticleCommande(models.Model):
    # L'article appartient à une commande (via related_name='items')
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='items')
    
    # Lien vers le produit d'origine (protégé contre la suppression)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)

    # Prix et quantité au moment de la commande (copie pour l'historique)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Article de Commande"
        verbose_name_plural = "Articles de Commande"

    def __str__(self):
        return f'{self.produit.nom} x{self.quantite}'

    def get_cost(self):
        # Coût total pour cet article spécifique
        return self.prix * self.quantite