from django import forms
from .models import OperatingSystem


#Form pour la création
class CreateVMForm(forms.Form):
    vmid = forms.IntegerField(label='ID')
    vm_name = forms.CharField(label='Nom', max_length=100)
    memory = forms.IntegerField(label='Mémoire')
    cores = forms.IntegerField(label='Nombre_de_coeurs')

#Form pour les OSs
class OSForm(forms.ModelForm):
    class Meta:
        model = OperatingSystem
        fields = ['name', 'name_os'] 

#Form pour supprimer une VM
class SupprimerVMForm(forms.Form):
    vms_a_supprimer = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, vms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vm_choices = [(str(vm['vmid']), vm['name']) for vm in vms]
        self.fields['vms_a_supprimer'].choices = vm_choices

#Form pour modifier une VM
class ModifierVMForm(forms.Form):
    vmid = forms.IntegerField(widget=forms.HiddenInput())
    nouveau_nom = forms.CharField(label='Nouveau nom', max_length=100, required=False)
    nouvelle_memoire = forms.IntegerField(label='Nouvelle mémoire (Mo)', required=False)
    nouveaux_cores = forms.IntegerField(label='Nouveaux cœurs', required=False)

#Form pour la suppresion
class SupprimerOSForm(forms.Form):
    os_a_supprimer = forms.ModelMultipleChoiceField(
        queryset=OperatingSystem.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
