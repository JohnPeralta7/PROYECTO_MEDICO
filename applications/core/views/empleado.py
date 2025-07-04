from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.forms.empleado import EmpleadoForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )


#VISTAS DE EMPLEADO

class EmpleadoListView(PermissionMixin, ListViewMixin, ListView):
    model = Empleado
    template_name = 'core/empleado/empleadolistview.html'
    context_object_name = 'empleado'
    permission_required = 'view_empleado'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(nombres__icontains=q) | 
                           Q(apellidos__icontains=q) | 
                           Q(cedula_ecuatoriana__icontains=q) | 
                           Q(dni__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(activo=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(activo=False), Q.AND)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_empleado'] = reverse_lazy('core:empleado_create')
        
        # Agregamos estadísticas para el dashboard
        context['total_empleado'] = Empleado.objects.count()
        context['active_empleado'] = Empleado.objects.filter(activo=True).count()
        
        
        return context


class EmpleadoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Empleado
    template_name = 'core/empleado/empleadocreate.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'add_empleado'

    def form_valid(self, form):
        self.object = form.save()
        empleado_name = f"{self.object.nombres} {self.object.apellidos}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al crear el empleado {empleado_name}.")
        return response

class EmpleadoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    template_name = 'core/empleado/empleadoupdate.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'change_empleado'

    def form_valid(self, form):
        empleado_name = f"{self.object.nombres} {self.object.apellidos}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al actualizar el empleado {empleado_name}.")
        return response

class EmpleadoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'delete_empleado'

    def post(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        empleado_name = f"{empleado.nombres} {empleado.apellidos}"
        empleado.delete()  # Si usas borrado lógico, pon aquí tu lógica
        messages.success(request, f"Empleado {empleado_name} eliminado correctamente.")
        return redirect(reverse_lazy('core:empleado_list'))

    def get(self, request, pk):
        # Si alguien entra por GET, simplemente redirige a la lista
        return redirect(reverse_lazy('core:empleado_list'))
    
    