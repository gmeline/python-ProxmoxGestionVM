from django.contrib import messages
import proxmoxer
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from .models import OperatingSystem
from .Forms import CreateVMForm, OSForm,SupprimerVMForm, ModifierVMForm, SupprimerOSForm
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from allauth.account.views import SignupView, LoginView, LogoutView

#Classe pour la page d'accueil
class IndexView(TemplateView):
    template_name = 'index.html'

#Classe qui permet de voir la liste des VM
class ListeVMView(TemplateView):
    template_name = 'liste_vm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Mise en place de la librairie ProxmoxAPI
        api = proxmoxer.ProxmoxAPI(
            host='192.168.1.197',
            user='root@pam',
            password='vivien',
            verify_ssl=False
        )

        vms = []
        for node in api.nodes.get():
            for vm in api.nodes(node["node"]).qemu.get():
                vms.append({
                    "vmid": vm["vmid"],
                    "name": vm["name"],
                    "status": vm["status"],
                })

        context['vms'] = vms
        return context

#Classe qui permet de créer la liste des OSs
class OSListView(ListView):
    model = OperatingSystem
    template_name = 'liste_os.html'
    context_object_name = 'liste_os'

#Classe qui permet de créer des VMs    
class CreateVMView(View):
    template_name = 'creer_vm.html'

    def get(self, request, *args, **kwargs):
        form = CreateVMForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateVMForm(request.POST)
        if form.is_valid():
            vm_name = form.cleaned_data['vm_name']
            memory = form.cleaned_data['memory']
            cores = form.cleaned_data['cores']
            vmid = form.cleaned_data['vmid']

            self.create_vm(vm_name, memory, cores, vmid)

            # Rediriger vers la page liste_vm avec un message de succès
            return HttpResponseRedirect(reverse('liste_vm') + '?success_message=VM%20cr%C3%A9%C3%A9e%20avec%20succ%C3%A8s')

        return render(request, self.template_name, {'form': form})
    
    def create_vm(self, vm_name, memory, cores, vmid):
        api = proxmoxer.ProxmoxAPI(
            host='192.168.1.197',
            user='root@pam',
            password='vivien',
            verify_ssl=False
        )
        api.nodes('pve').qemu.create(vmid=vmid, name=vm_name, memory=int(memory), cores=int(cores))

#Classe qui permet de créer des OSs
class CreateOSView(CreateView):
    model = OperatingSystem
    form_class = OSForm
    template_name = 'creer_os.html'
    success_url = '/liste_os/'

#Classe qui permet de supprimer une VM
class SupprimerVMView(View):
    template_name = 'supprimer_vm.html'

    def get(self, request, *args, **kwargs):
        api = proxmoxer.ProxmoxAPI(
            host='192.168.1.197',
            user='root@pam',
            password='vivien',
            verify_ssl=False
        )
        vms = []
        for node in api.nodes.get():
            for vm in api.nodes(node["node"]).qemu.get():
                vms.append({
                    "vmid": vm["vmid"],
                    "name": vm["name"],
                    "status": vm["status"],
                })

        form = SupprimerVMForm(vms)

        context = {
            'vms': vms,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        api = proxmoxer.ProxmoxAPI(
            host='192.168.1.197',
            user='root@pam',
            password='vivien',
            verify_ssl=False
        )
        vms = []
        for node in api.nodes.get():
            for vm in api.nodes(node["node"]).qemu.get():
                vms.append({
                    "vmid": vm["vmid"],
                    "name": vm["name"],
                    "status": vm["status"],
                })

        form = SupprimerVMForm(vms, request.POST)

        if form.is_valid():
            vms_selected = form.cleaned_data['vms_a_supprimer']

            if vms_selected:
                for vm_id in vms_selected:
                    try:
                        api.nodes('pve').qemu(vm_id).delete()
                    except Exception as e:
                        print("Erreur lors de la suppression :", e)
                        # Vous pouvez ajouter un message d'erreur ici si nécessaire
                        return redirect('liste_vm')

                # Message de succès dans la chaîne de requête
                success_message = f"La machine virtuelle {', '.join(vms_selected)} a été supprimée avec succès."
                return HttpResponseRedirect(reverse('liste_vm') + f"?success_message={success_message}")

        return redirect('liste_vm')

#Classe qui permet de modifier une VM
class ModifierVMView(View):
    template_name = 'modifier_vm.html'

    def get(self, request, *args, **kwargs):
        vmid = kwargs.get('vmid')
        api = proxmoxer.ProxmoxAPI(
            host='192.168.1.197',
            user='root@pam',
            password='vivien',
            verify_ssl=False
        )

        vm = api.nodes('pve').qemu(vmid).get()

        form = ModifierVMForm(initial={
            'vmid': vm[0].get('vmid') if vm and 'vmid' in vm[0] else None,
            'nouveau_nom': vm[0].get('name', ''),
            'nouvelle_memoire': vm[0].get('memory', ''),
            'nouveaux_cores': vm[0].get('cores', '')
        })

        context = {
            'vm': vm,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ModifierVMForm(request.POST)

        if form.is_valid():
            vmid = form.cleaned_data['vmid']
            nouveau_nom = form.cleaned_data['nouveau_nom']
            nouvelle_memoire = form.cleaned_data['nouvelle_memoire']
            nouveaux_cores = form.cleaned_data['nouveaux_cores']

            api = proxmoxer.ProxmoxAPI(
                host='192.168.1.197',
                user='root@pam',
                password='vivien',
                verify_ssl=False
            )

            try:
                vm = api.nodes('pve').qemu(vmid)

                print("Avant la mise à jour - Nom:", vm.get('name'))
                print("Avant la mise à jour - Mémoire:", vm.get('memory'))
                print("Avant la mise à jour - Cores:", vm.get('cores'))

                vm.set(name=nouveau_nom, memory=nouvelle_memoire, cores=nouveaux_cores)

                print("Après la mise à jour - Nom:", vm.get('name'))
                print("Après la mise à jour - Mémoire:", vm.get('memory'))
                print("Après la mise à jour - Cores:", vm.get('cores'))

                print("Mise à jour réussie")
            except Exception as e:
                print("Erreur lors de la mise à jour :", e)

        return redirect('liste_vm')
    
#Classe qui permet de s'inscrire
class CustomSignupView(SignupView):
    template_name = 'account/signup.html'

#Classe qui permet de se connecter
class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def form_invalid(self, form):
        messages.warning(self.request, "Merci de vous connecter pour accéder à cette page.")
        return super().form_invalid(form)
    
#Classe qui permet de se déconnecter
class CustomLogoutView(LogoutView):
    template_name = 'account/logout.html'  # Vous pouvez conserver cela si nécessaire
    next_page = '/'  # Spécifiez la page de redirection après la déconnexion

    def get(self, request, *args, **kwargs):
        # Vous pouvez ajouter du code supplémentaire ici si nécessaire
        return super().get(request, *args, **kwargs)

class ProfileView(View):
    template_name = 'profile.html'  # Assurez-vous d'avoir un template correspondant

    def get(self, request, *args, **kwargs):
        # Ajoutez ici la logique pour récupérer les données du profil
        context = {
            'user': request.user,
            # Ajoutez d'autres données de profil si nécessaire
        }
        return render(request, self.template_name, context)
    
class SupprimerOSView(ListView):
    model = OperatingSystem
    template_name = 'supprimer_os.html'
    context_object_name = 'liste_vos'
    http_method_names = ['get', 'post']  # Ajoutez 'post' à la liste des méthodes autorisées

    def post(self, request, *args, **kwargs):
        form = SupprimerOSForm(request.POST)
        if form.is_valid():
            os_a_supprimer = form.cleaned_data['os_a_supprimer']
            os_a_supprimer.delete()
            return redirect('liste_os')  # Redirige vers la liste principale après la suppression
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SupprimerOSForm()
        return context