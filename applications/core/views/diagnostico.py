from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from applications.core.forms.diagnostico import DiagnosticoForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )


#VISTAS DE DIAGNOSTICO

class DiagnosticoListView(PermissionMixin, ListViewMixin, ListView):
    model = Diagnostico
    template_name = 'core/diagnostico/diagnosticolistview.html'
    context_object_name = 'diagnostico'
    permission_required = 'view_diagnosis'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(codigo__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(activo=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(activo=False), Q.AND)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:diagnosis_create')       
        return context


class DiagnosticoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    template_name = 'core/diagnostico/diagnosticocreate.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'add_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al crear el diagnóstico {self.object.codigo}.")
        return response


class DiagnosticoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    template_name = 'core/diagnostico/diagnosticoupdate.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'change_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al actualizar el diagnóstico {self.object.codigo}.")
        return response


class DiagnosticoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'delete_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Diagnóstico'
        context['description'] = f"¿Desea eliminar el diagnóstico: {self.object.codigo} - {self.object.descripcion}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el diagnóstico {self.object.codigo}.")
        return response