from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.db.models import Q
from applications.doctor.forms.servicios import ServiciosAdicionalesForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    ServiciosAdicionales
    )


#VISTAS DE EMPLEADO


class ServiciosAdicionalesListView(PermissionMixin, ListViewMixin, ListView):

    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/servicios_adicionaleslistview.html'
    context_object_name = 'servicios_adicionales'
    permission_required = 'view_servicios_adicionales'

    def get_queryset(self):
        queryset = self.model.objects.all()
        q = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()

        # Filtrar por término de búsqueda (nombre o descripción)
        if q:
            queryset = queryset.filter(
                Q(nombre_servicio__icontains=q) |
                Q(descripcion__icontains=q)
            )

        # Filtrar por estado
        if status == 'active':
            queryset = queryset.filter(activo=True)
        elif status == 'inactive':
            queryset = queryset.filter(activo=False)

        return queryset.order_by('id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_servicios_adicionales'] = reverse_lazy('doctor:servicios_adicionales_create')
        return context


class ServiciosAdicionalesCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/servicios_create.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('doctor:servicios_adicionales_list')
    permission_required = 'add_serviciosadicionales'

    def form_valid(self, form):
        messages.success(self.request, "Servicio adicional creado correctamente.")
        return super().form_valid(form)


class ServiciosAdicionalesUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/servicios_update.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('doctor:servicios_adicionales_list')
    permission_required = 'change_serviciosadicionales'

    def form_valid(self, form):
        messages.success(self.request, "Servicio adicional actualizado correctamente.")
        return super().form_valid(form)

class ServiciosAdicionalesDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:servicios_adicionales_list')
    permission_required = 'delete_serviciosadicionales'

    def form_valid(self, form):
        messages.success(self.request, "Servicio adicional eliminado correctamente.")
        return super().form_valid(form)

