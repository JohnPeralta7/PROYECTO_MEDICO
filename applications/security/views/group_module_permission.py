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
        
        # Iniciar con la consulta base - CARGAR TODOS LOS REGISTROS
        queryset = self.model.objects.select_related('group', 'module').prefetch_related('permissions', 'module__permissions')
        
        # Solo aplicar filtros si hay parámetros específicos
        has_filters = bool(q or grupo or modulo)
        
        if has_filters:
            filters = Q()
            
            # Filtrar por término de búsqueda
            if q:
                filters |= (Q(group__name__icontains=q) | 
                           Q(module__name__icontains=q) |
                           Q(module__menu__name__icontains=q))
            
            # Filtrar por grupo
            if grupo:
                filters &= Q(group__id=grupo)
            
            # Filtrar por módulo
            if modulo:
                filters &= Q(module__id=modulo)
            
            queryset = queryset.filter(filters)
            
        return queryset.order_by('group__name', 'module__name')

    def get_context_data(self, **kwargs):
        from django.contrib.auth.models import Group
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        
        # Agregar todos los grupos disponibles para el selector
        context['all_groups'] = Group.objects.all().order_by('name')
        
        # FORZAR los datos para asegurar que lleguen al template
        queryset = self.get_queryset()
        context['group_module_permissions'] = queryset
        
        # DEBUG: Verificar datos
        print(f"=== DEBUG VISTA GET_CONTEXT_DATA ===")
        print(f"QuerySet count: {queryset.count()}")
        print(f"Context group_module_permissions count: {context['group_module_permissions'].count()}")
        
        if queryset.exists():
            print("✅ Datos encontrados:")
            for gmp in queryset[:5]:  # Mostrar primeros 5
                print(f"  • Grupo: {gmp.group.name} -> Módulo: {gmp.module.name} -> Permisos: {gmp.permissions.count()}")
        else:
            print("❌ NO hay datos en el queryset")
            # Verificar directamente en BD
            total_bd = GroupModulePermission.objects.count()
            print(f"Total en BD: {total_bd}")
            if total_bd > 0:
                print("❌ PROBLEMA: Hay datos en BD pero no llegan al queryset")
                # Forzar todos los datos
                context['group_module_permissions'] = GroupModulePermission.objects.select_related(
                    'group', 'module', 'module__menu'
                ).prefetch_related('permissions', 'module__permissions').all()
                print(f"✅ FORZADO: {context['group_module_permissions'].count()} registros")
        
        print(f"Grupos disponibles: {[g.name for g in context['all_groups']]}")
        print("=== FIN DEBUG VISTA ===")
        
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
