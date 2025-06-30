from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )


#VISTAS DE Gasto Mensual

class GastoMensualListView(ListView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/gasto_mensuallistview.html'
    context_object_name = 'gastomensual'
    permission_required = 'view_gastomensual'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(tipo_gasto__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:gastomensual_create')
        
        # Agregamos estadísticas para el dashboard
        context['total_gastomensual'] = GastoMensual.objects.count()
        
        
        return context


class GastoMensualCreateView(CreateView):
    ...

class GastoMensualUpdateView(UpdateView):
    ...

class GastoMensualDeleteView(DeleteView):
    ...