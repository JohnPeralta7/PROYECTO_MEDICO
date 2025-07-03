from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.forms.horario import HorarioAtencionForm, HorarioAtencionEditForm
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
        """Crear múltiples horarios para los días seleccionados"""
        dias_seleccionados = form.cleaned_data['dias_semana']
        hora_inicio = form.cleaned_data['hora_inicio']
        hora_fin = form.cleaned_data['hora_fin']
        intervalo_desde = form.cleaned_data.get('intervalo_desde')
        intervalo_hasta = form.cleaned_data.get('intervalo_hasta')
        activo = form.cleaned_data['activo']
        
        horarios_creados = []
        horarios_existentes = []
        
        for dia in dias_seleccionados:
            # Verificar si ya existe un horario para este día con las mismas horas
            if HorarioAtencion.objects.filter(
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            ).exists():
                horarios_existentes.append(dia)
                continue
            
            # Crear el horario para este día
            horario = HorarioAtencion.objects.create(
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                intervalo_desde=intervalo_desde,
                intervalo_hasta=intervalo_hasta,
                activo=activo
            )
            horarios_creados.append(dia)
        
        # Mensajes de feedback
        if horarios_creados:
            dias_creados = ', '.join([dict(self.form_class.base_fields['dias_semana'].choices)[dia] for dia in horarios_creados])
            messages.success(self.request, f"Horarios creados exitosamente para: {dias_creados}")
        
        if horarios_existentes:
            dias_existentes = ', '.join([dict(self.form_class.base_fields['dias_semana'].choices)[dia] for dia in horarios_existentes])
            messages.warning(self.request, f"Ya existen horarios similares para: {dias_existentes}")
        
        if not horarios_creados and not horarios_existentes:
            messages.error(self.request, "No se pudieron crear los horarios.")
        
        return redirect(self.success_url)

class HorarioAtencionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/horario_update.html'
    form_class = HorarioAtencionEditForm  # Usar el formulario de edición individual
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

