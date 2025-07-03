from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )
from applications.core.forms.doctor import DoctorForm


#VISTAS DE DOCTOR

class DoctorListView(ListView):
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


class DoctorCreateView(CreateView):
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


class DoctorUpdateView(UpdateView):
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
        context['title'] = f'Editar Doctor: {self.object.nombre_completo}'
        context['list_url'] = reverse_lazy('core:doctor_list')
        return context


class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'core/doctor/doctor_delete.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        # En lugar de eliminar, desactivar el doctor
        self.object.activo = False
        self.object.save()
        
        messages.success(request, f'Doctor {self.object.nombre_completo} desactivado exitosamente.')
        return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Desactivar Doctor: {self.object.nombre_completo}'
        context['list_url'] = reverse_lazy('core:doctor_list')
        return context


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