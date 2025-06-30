from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )


#VISTAS DE MEDICAMENTO

class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'core/medicamento/medicamentolistview.html'
    context_object_name = 'medicamentos'
    permission_required = 'view_medicamento'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(marca_medicamento__icontains=q) | 
                           Q(nombre__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(activo=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(activo=False), Q.AND)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:medicamento_create')
        
        # Agregamos estadísticas para el dashboard
        context['total_medicamentos'] = Medicamento.objects.count()
        context['active_medicamentos'] = Medicamento.objects.filter(activo=True).count()
        
        
        return context


class MedicamentoCreateView(CreateView):
    ...

class MedicamentoUpdateView(UpdateView):
    ...

class MedicamentoDeleteView(DeleteView):
    ...