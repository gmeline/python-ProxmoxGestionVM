from django.urls import path, include
from .views import IndexView,ListeVMView, OSListView, CreateVMView, CreateOSView,SupprimerVMView, ModifierVMView, CustomSignupView,CustomLoginView,CustomLogoutView, ProfileView, SupprimerOSView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='accueil'),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
    path('liste_vm/', ListeVMView.as_view(), name='liste_vm'),
    path('liste_os/', OSListView.as_view(), name='liste_os'),
    path('creer_vm/', CreateVMView.as_view(), name='creer_vm'),
    path('creer_os/', CreateOSView.as_view(), name='creer_os'),
    path('supprimer_vm/', SupprimerVMView.as_view(), name='supprimer_vm'),
    path('modifier_vm/<int:vmid>/', ModifierVMView.as_view(), name='modifier_vm'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('supprimer_os/', SupprimerOSView.as_view(), name='supprimer_os'),
]
