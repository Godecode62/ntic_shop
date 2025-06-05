from django.shortcuts import render , get_object_or_404
from django.urls import reverse_lazy
from .models import Produit
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView, TemplateView
from boutique.forms import ProduitForm
from django.contrib.auth.mixins import UserPassesTestMixin
from boutique.models import Categorie
from django.db.models import Q


# Classe qui verifie que l'utilisateur est connecté et qu'il est un admin
class UserAdminRequired(UserPassesTestMixin):
    login_url = reverse_lazy('login')
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff and self.request.user.is_superuser



#Action qui necessite que l'utilisateur soit connecté et qu'il soit un admin

class AdminDashboard(UserAdminRequired, TemplateView):
    template_name = 'boutique/admin_dashboard.html'
    

class CreateProduit(UserAdminRequired,CreateView):
    form_class = ProduitForm
    template_name = "boutique/produit_create.html"
    success_url = reverse_lazy('liste_produits')
    queryset = Produit.objects.all()


class ProductDelete(UserAdminRequired,DeleteView):
    queryset = Produit.objects.all()
    template_name = 'boutique/delete_produit.html'
    

class PruduitUpdate(UserAdminRequired,UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'boutique/produit_update.html'
    success_url = reverse_lazy('liste_produits')

    def get_object(self, queryset=None):
        return get_object_or_404(Produit, pk=self.kwargs.get('pk'))



#Action qui ne necessite pas que l'utilisateur soit connecté

class ProductList(ListView):
    queryset = Produit.objects.all()
    template_name = "boutique/liste_produits.html"
    paginate_by = 6
    
    

class ProductList(ListView):
    
    template_name = "boutique/liste_produits.html"
    context_object_name = 'object_list'
    paginate_by = 6 

    def get_queryset(self):
       
        # Commence par tous les produits disponibles, triés par date d'ajout
        queryset = Produit.objects.order_by('-date_ajout')
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            # Récupère l'objet Categorie correspondant au slug, ou lève 404
            self.current_category = get_object_or_404(Categorie, slug=category_slug)
            # Filtre le queryset pour n'inclure que les produits de cette catégorie
            queryset = queryset.filter(categorie=self.current_category)
        else:
            self.current_category = None

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) | Q(description__icontains=query)
            ).distinct() # `distinct()` pour éviter les doublons si le même terme est dans nom ET description

        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires au contexte du template.
        """
        context = super().get_context_data(**kwargs)
        
        # Passe l'objet de la catégorie actuelle au template.
        # Utile pour changer le titre de la page par exemple ("Nos Produits" vs "Produits - Électronique")
        context['current_category'] = self.current_category
        
        # Optionnel mais recommandé : passer toutes les catégories pour la navbar.
        # Si tu as un context processor pour ça, tu peux supprimer cette ligne.
        context['all_categories'] = Categorie.objects.all().order_by('nom') 
        
        return context


class ProduitDetail(DetailView):
    queryset = Produit.objects.all()
    template_name = 'boutique/detail_produit.html'



#Action qui ne necessite pas que l'utilisateur soit connecté
def home_page_view(request):
    # Récupère les derniers produits ajoutés (les 8 derniers)
    nouveaux_produits = Produit.objects.order_by('-date_ajout')[:8]

    context = {
        'nouveaux_produits': nouveaux_produits
    }
    return render(request, 'index.html', context)
