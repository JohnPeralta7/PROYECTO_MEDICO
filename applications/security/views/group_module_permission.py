from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from applications.security.components.mixin_crud import (
    CreateViewMixin, 
    DeleteViewMixin, 
    ListViewMixin, 
    PermissionMixin, 
    UpdateViewMixin
)
from applications.security.models import GroupModulePermission, Module
from applications.security.forms.group_module_permission import GroupModulePermissionForm

class GroupModulePermissionListView( PermissionMixin, ListViewMixin, ListView):
    """
    Vista para listar asignaciones de permisos a grupo-módulo
    """
    model = GroupModulePermission
    template_name = 'security/group_module_permission/list.html'  # template a crear después
    context_object_name = 'group_module_permissions'
    permission_required = 'view_groupmodulepermission'
    #breadcrumb_title = 'Lista de Permisos por Grupo y Módulo'

    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo = self.request.GET.get('grupo')
        modulo = self.request.GET.get('modulo')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.select_related('group', 'module')
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(group__name__icontains=q) | 
                           Q(module__name__icontains=q) |
                           Q(module__menu__name__icontains=q), Q.AND)
        
        # Filtrar por grupo
        if grupo:
            self.query.add(Q(group__id=grupo), Q.AND)
        
        # Filtrar por módulo
        if modulo:
            self.query.add(Q(module__id=modulo), Q.AND)
            
        return queryset.filter(self.query).order_by('group__name', 'module__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        return context


class GroupModulePermissionCreateView( PermissionMixin, CreateViewMixin, CreateView):
    """
    Vista para crear asignación de permisos a grupo-módulo
    """
    model = GroupModulePermission
    form_class = GroupModulePermissionForm
    template_name = 'security/group_module_permission/form.html'  # template a crear después
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'add_groupmodulepermission'
    #breadcrumb_title = 'Asignar Nuevos Permisos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Asignar Permisos'
        context['back_url'] = self.success_url
        # Obtener módulos para JavaScript
        context['modules_json'] = list(Module.objects.values('id', 'name'))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group_module_permission = self.object
        messages.success(
            self.request, 
            f"Éxito al asignar permisos del grupo {group_module_permission.group.name} al módulo {group_module_permission.module.name}."
        )
        return response


class GroupModulePermissionUpdateView( PermissionMixin, UpdateViewMixin, UpdateView):
    """
    Vista para actualizar asignación de permisos a grupo-módulo
    """
    model = GroupModulePermission
    form_class = GroupModulePermissionForm
    template_name = 'security/group_module_permission/form.html'
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'change_groupmodulepermission'    
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #self.breadcrumb_title = self.get_breadcrumb_title()
        context['grabar'] = 'Actualizar Permisos'
        context['back_url'] = self.success_url
        # Obtener módulos para JavaScript
        context['modules_json'] = list(Module.objects.values('id', 'name'))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group_module_permission = self.object
        messages.success(
            self.request, 
            f"Éxito al actualizar permisos del grupo {group_module_permission.group.name} en módulo {group_module_permission.module.name}."
        )
        return response


class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    """
    Vista para eliminar asignación de permisos a grupo-módulo
    """
    model = GroupModulePermission
    template_name = 'fragments/delete.html'  # Usando el template genérico de borrado
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'delete_groupmodulepermission'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #self.breadcrumb_title = self.get_breadcrumb_title()
        context['title'] = f"Eliminar Asignación de Permisos"
        context['description'] = f"¿Desea eliminar los permisos del grupo '{self.object.group.name}' para el módulo '{self.object.module.name}'?"
        context['back_url'] = self.success_url
        return context
    
    def post(self, request, *args, **kwargs):
        group_module_permission = self.get_object()
        group_name = group_module_permission.group.name
        module_name = group_module_permission.module.name
        
        response = super().post(request, *args, **kwargs)
        messages.success(
            request,
            f"Asignación de permisos del grupo {group_name} al módulo {module_name} eliminada exitosamente."
        )
        return response
