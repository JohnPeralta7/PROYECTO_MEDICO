from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    CitaMedica
    )


#VISTAS DE EMPLEADO

class CitaMedicaListView(ListView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/cita_medicalistview.html'
    context_object_name = 'cita_medica'
    permission_required = 'view_cita_medica'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(paciente__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_cita_medica'] = reverse_lazy('doctor:cita_medica_create')
        
        
        
        return context


class CitaMedicaCreateView(CreateView):
    ...

class CitaMedicaUpdateView(UpdateView):
    ...

class CitaMedicaDeleteView(DeleteView):
    ...