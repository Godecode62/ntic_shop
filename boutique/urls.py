from django.urls import path
from . import views



urlpatterns = [
    path('',views.home_page_view, name='home'),
    path('product_list', views.ProductList.as_view(), name='liste_produits'),
    path('produit/<int:pk>/', views.ProduitDetail.as_view(), name='produit_detail'),
    path('create/',views.CreateProduit.as_view(), name='create_produit'),
    path('delete/',views.ProductDelete.as_view(),name='delete_produit'),
    path('update/<int:pk>/', views.PruduitUpdate.as_view(), name='update_produit'),
    path('admin_dashboard/', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('produits/categorie/<slug:category_slug>/', views.ProductList.as_view(), name='produits_par_categorie'),
]

