from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from compte.forms import UserRegistrationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login


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
    
    

class UserRegistrationView(FormView):
    """
    Vue générique basée sur FormView pour l'inscription des utilisateurs.
    """
    template_name = 'compte/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Cette méthode est appelée lorsque le formulaire est valide.
        Elle crée l'utilisateur et le connecte.
        """
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
