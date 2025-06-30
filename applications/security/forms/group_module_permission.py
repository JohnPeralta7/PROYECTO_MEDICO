from django import forms
from django.contrib.auth.models import Group, Permission
from applications.security.models import Module, GroupModulePermission

class GroupModulePermissionForm(forms.ModelForm):
    """
    Formulario para la creación y edición de permisos de grupo-módulo
    """
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        label="Grupo", 
        widget=forms.Select(attrs={
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
        })
    )
    
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(), 
        label="Módulo", 
        widget=forms.Select(attrs={
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
        })
    )
    
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        label="Permisos",
        widget=forms.SelectMultiple(attrs={
            "class": "block w-full py-3 px-4 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            "size": "5"
        })
    )

    class Meta:
        model = GroupModulePermission
        fields = ["group", "module", "permissions"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar los permisos según el módulo seleccionado si existe
        if self.instance.pk:
            self.fields['permissions'].queryset = self.instance.module.permissions.all()
            
    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        module = cleaned_data.get('module')
        
        if group and module:
            # Verificar restricción unique de grupo y módulo
            if GroupModulePermission.objects.filter(group=group, module=module).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
                self.add_error('module', "Ya existe una asignación para este grupo y módulo.")
                
        return cleaned_data
