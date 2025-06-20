from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from compte.forms import UserRegistrationForm, UserUpdateForm
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.views.generic import DetailView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from compte.forms import CustomPasswordChangeForm

from compte.models import User
from boutique.views import UserAdminRequired


#Ce machin necessite que le user soit admin et qu'il soit connecté
class AllUsers(UserAdminRequired, ListView):
    queryset = User.objects.all()
    template_name = 'compte/all_users.html'


#Pareil pour celui-ci 
class DeleteUser(UserAdminRequired, DeleteView):
    model = User
    template_name = 'compte/delete_user.html'
    success_url = reverse_lazy('show_all_users')

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

    template_name = 'compte/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ShhowMyAccount(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'compte/my_account.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    

class UserAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'compte/edit_account.html'
    # Pour que le template puisse accéder à l'objet user
    context_object_name = 'user'
    # Redirige vers la page de mon compte après succès
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        # S'assure que l'utilisateur ne peut modifier que son propre compte
        return self.request.user

    # hum ca c'est chelou, mais je crois que c'est pour passer l'instance de l'utilisateur au formulaire
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    
    
    
class ChangeUserPassword(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'compte/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    
    
class ChangeUserPasswordDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'compte/password_change_done.html'
    
