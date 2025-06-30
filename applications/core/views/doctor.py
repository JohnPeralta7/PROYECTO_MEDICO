from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )


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
    ...

class DoctorUpdateView(UpdateView):
    ...

class DoctorDeleteView(DeleteView):
    ...