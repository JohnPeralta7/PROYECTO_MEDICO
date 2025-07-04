from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )
from applications.core.forms.doctor import DoctorForm


#VISTAS DE DOCTOR

class DoctorListView(PermissionMixin, ListViewMixin, ListView):
    model = Doctor
    template_name = 'core/doctor/doctorlistview.html'
    context_object_name = 'doctor'
    permission_required = 'view_doctor'
    

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
                           Q(codigo_unico_doctor__icontains=q) | 
                           Q(ruc__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(activo=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(activo=False), Q.AND)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_doctor'] = reverse_lazy('core:doctor_create')
        
        # Agregamos estadísticas para el dashboard
        context['total_doctor'] = Doctor.objects.count()
        context['active_doctor'] = Doctor.objects.filter(activo=True).count()
        
        
        return context


class DoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/doctor_create.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'add_doctor'

    def form_valid(self, form):
        messages.success(self.request, f'Doctor {form.instance.nombre_completo} creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Doctor'
        context['list_url'] = reverse_lazy('core:doctor_list')
        return context


class DoctorUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/doctor_update.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'change_doctor'

    def form_valid(self, form):
        messages.success(self.request, f'Doctor {form.instance.nombre_completo} actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Doctor'
        context['list_url'] = reverse_lazy('core:doctor_list')
        return context

class DoctorDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()
        messages.success(request, f'Doctor {doctor.nombre_completo} eliminado exitosamente.')
        return redirect(reverse_lazy('core:doctor_list'))

    def get(self, request, pk):
        # Si alguien entra por GET, simplemente redirige a la lista
        return redirect(reverse_lazy('core:doctor_list'))


@login_required
@require_http_methods(["POST"])
def doctor_create_ajax(request):
    """Vista AJAX para crear doctor desde el modal"""
    form = DoctorForm(request.POST, request.FILES)
    
    if form.is_valid():
        doctor = form.save()
        messages.success(request, f'Doctor {doctor.nombre_completo} creado exitosamente.')
        
        return JsonResponse({
            'success': True,
            'message': f'Doctor {doctor.nombre_completo} creado exitosamente.',
            'doctor_id': doctor.pk,
            'redirect_url': reverse_lazy('core:doctor_list')
        })
    else:
        # Preparar errores para envío por AJAX
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list
            
        return JsonResponse({
            'success': False,
            'errors': errors,
            'message': 'Por favor corrige los errores en el formulario.'
        }, status=400)
        
@login_required
@require_http_methods(["POST"])
def doctor_update_ajax(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST, request.FILES, instance=doctor)
    if form.is_valid():
        doctor = form.save()
        messages.success(request, f'Doctor {doctor.nombre_completo} actualizado exitosamente.')
        return JsonResponse({
            'success': True,
            'message': f'Doctor {doctor.nombre_completo} actualizado exitosamente.',
            'doctor_id': doctor.pk,
            'redirect_url': reverse_lazy('core:doctor_list')
        })
    else:
        errors = {field: error_list for field, error_list in form.errors.items()}
        return JsonResponse({
            'success': False,
            'errors': errors,
            'message': 'Por favor corrige los errores en el formulario.'
        }, status=400)
        
@login_required
@require_http_methods(["GET"])
def doctor_detail_ajax(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    # Si el campo especialidad es ManyToMany, usa .all()
    especialidades = [e.nombre for e in doctor.especialidad.all()] if hasattr(doctor, 'especialidad') else []
    return JsonResponse({
        'nombre_completo': getattr(doctor, 'nombre_completo', ''),
        'codigo_unico_doctor': getattr(doctor, 'codigo_unico_doctor', ''),
        'ruc': getattr(doctor, 'ruc', ''),
        'email': getattr(doctor, 'email', ''),
        'telefonos': getattr(doctor, 'telefonos', ''),
        'duracion_atencion': getattr(doctor, 'duracion_atencion', ''),
        'activo': getattr(doctor, 'activo', False),
        'especialidades': especialidades,
        'fecha_nacimiento': doctor.fecha_nacimiento.strftime('%Y-%m-%d') if getattr(doctor, 'fecha_nacimiento', None) else '',
        'direccion': getattr(doctor, 'direccion', ''),
        'horario_atencion': getattr(doctor, 'horario_atencion', ''),
        'descripcion': getattr(doctor, 'descripcion', ''),
        'foto_url': doctor.foto.url if getattr(doctor, 'foto', None) else '',
    })