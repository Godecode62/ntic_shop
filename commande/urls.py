from django.urls import path
from commande import views

urlpatterns = [
    path('creer/', views.creer_commande, name='creer_commande'),
    path('succes/<int:commande_id>/', views.commande_succes, name='commande_succes'),
    path('historique/', views.historique_commandes, name='historique_commandes'),
    path('annuler/<int:commande_id>/', views.annuler_commande, name='annuler_commande'),
    path('admin/commandes/', views.gestion_commandes_admin, name='gestion_commandes_admin'),
]
