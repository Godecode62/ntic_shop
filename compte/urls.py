from django.urls import path



from compte import views


urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/',views.UserRegistrationView.as_view(), name='register'),
    path('my_account/', views.ShhowMyAccount.as_view(), name='my_account'),
    path('update_account/', views.UserAccountUpdateView.as_view(), name='update_account'),
    path('password/change/',views.ChangeUserPassword.as_view(),name='password_change'),
    path('password/change/done/', views.ChangeUserPasswordDone.as_view(), name='password_change_done'),
    path('show/user/all/', views.AllUsers.as_view(), name='show_all_users'),
    path('delete/user/<int:pk>',views.DeleteUser.as_view(), name='delete_user'),
]
