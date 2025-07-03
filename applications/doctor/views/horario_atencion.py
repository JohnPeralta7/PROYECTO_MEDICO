from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.forms.horario import HorarioAtencionForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    HorarioAtencion
    )


#VISTAS DE EMPLEADO

class HorarioAtencionListView(PermissionMixin, ListViewMixin, ListView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/horario_atencionlistview.html'
    context_object_name = 'horario_atencion'
    permission_required = 'view_horario_atencion'

    def get_queryset(self):
        queryset = self.model.objects.all()
        status = self.request.GET.get('status', '').strip()

        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            queryset = queryset.filter(activo=True)
        elif status == 'inactive':
            queryset = queryset.filter(activo=False)

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_horario_atencion'] = reverse_lazy('doctor:horario_atencion_create')
        return context


class HorarioAtencionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/horario_create.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'add_horarioatencion'

    def form_valid(self, form):
        messages.success(self.request, "Horario de atención creado correctamente.")
        return super().form_valid(form)

class HorarioAtencionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/horario_update.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'change_horarioatencion'

    def form_valid(self, form):
        messages.success(self.request, "Horario de atención actualizado correctamente.")
        return super().form_valid(form)
    
class HorarioAtencionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = HorarioAtencion
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'delete_horarioatencion'

    def form_valid(self, form):
        messages.success(self.request, "Horario de atención eliminado correctamente.")
        return super().form_valid(form)