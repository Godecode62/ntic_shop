from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy



class LoginUser(LoginView):
    template_name = 'compte/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):

        if self.request.user.is_authenticated and self.request.user.is_staff and self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')

        return reverse_lazy('liste_produits')
    


class LogoutUser(LogoutView):
    # Redirige l'utilisateur vers la page d'accueil ou de connexion après déconnexion
    next_page = reverse_lazy('liste_produits')