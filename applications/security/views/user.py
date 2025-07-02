#Estudiar full esto
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from applications.security.components.mixin_crud import (
    CreateViewMixin, 
    DeleteViewMixin, 
    ListViewMixin, 
    PermissionMixin, 
    UpdateViewMixin
)
from applications.security.models import User
from applications.security.forms.user import UserForm
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    DetailView
)


class UserListView( PermissionMixin, ListViewMixin, ListView):
    """
    Vista para listar usuarios
    """
    template_name = 'security/users/list.html'
    model = User
    context_object_name = 'users'
    permission_required = 'view_user'
    

    def get_queryset(self):
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(username__icontains=q) | 
                           Q(first_name__icontains=q) | 
                           Q(last_name__icontains=q) | 
                           Q(email__icontains=q) | 
                           Q(dni__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(is_active=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(is_active=False), Q.AND)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        from django.contrib.auth.models import Group
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:user_create')
        
        # Agregamos estadísticas para el dashboard
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        context['staff_users'] = User.objects.filter(is_staff=True).count()
        
        # Agregar todos los grupos disponibles para el modal de creación
        context['available_groups'] = Group.objects.all().order_by('name')
        
        return context


class UserCreateView( PermissionMixin, CreateViewMixin, CreateView):    
    """
    Vista para crear usuarios
    """
    model = User
    template_name = 'security/users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'add_user'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        context['grabar'] = 'Crear Usuario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Usuario {user.get_full_name} creado con éxito.")
        return response


class UserUpdateView( PermissionMixin, UpdateViewMixin, UpdateView):    
    """
    Vista para actualizar usuarios
    """
    model = User
    template_name = 'security/users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'change_user'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #self.breadcrumb_title = self.get_breadcrumb_title()
        if 'form' not in context:
            context['form'] = self.get_form()
        context['grabar'] = 'Actualizar Usuario'
        context['back_url'] = self.success_url
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Usuario {user.get_full_name} actualizado con éxito.")
        return response


class UserDeleteView( PermissionMixin, DeleteViewMixin, DeleteView):
    """
    Vista para eliminar usuarios
    """
    model = User
    template_name = 'security/users/delete.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'delete_user'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #self.breadcrumb_title = self.get_breadcrumb_title()
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user_name = user.get_full_name
        
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, f"Usuario {user_name} eliminado con éxito.")
        return response


class UserDetailView(PermissionMixin, DetailView):
    """
    Vista para ver detalles de un usuario
    """
    model = User
    template_name = 'security/users/detail.html'
    context_object_name = 'user'
    permission_required = 'view_user'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #self.breadcrumb_title = self.get_breadcrumb_title()
        context['title'] = 'Detalle de Usuario'
        context['title1'] = f'Usuario: {self.object.get_full_name}'
        return context