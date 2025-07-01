from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    Pago
    )


#VISTAS DE EMPLEADO

class PagoListView(ListView):
    model = Pago
    template_name = 'doctor/pago/pagolistview.html'
    context_object_name = 'pago'
    permission_required = 'view_pago'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        
        
        # Filtrar por estado (activo/inactivo)
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_pago'] = reverse_lazy('doctor:pago_create')
        
        
        
        return context


class PagoCreateView(CreateView):
    ...

class PagoUpdateView(UpdateView):
    ...

class PagoDeleteView(DeleteView):
    ...