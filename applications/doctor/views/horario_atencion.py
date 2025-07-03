from django.http import JsonResponse
from django.urls import reverse_lazy
<<<<<<< HEAD
from django.db.models import Q
=======
from django.contrib import messages
from django.db.models import Q
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.forms.horario import HorarioAtencionForm
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    HorarioAtencion
    )


#VISTAS DE EMPLEADO

<<<<<<< HEAD
class HorarioAtencionListView(ListView):
=======
class HorarioAtencionListView(PermissionMixin, ListViewMixin, ListView):
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/horario_atencionlistview.html'
    context_object_name = 'horario_atencion'
    permission_required = 'view_horario_atencion'
<<<<<<< HEAD
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        
        
        # Filtrar por estado (activo/inactivo)
        return queryset.filter(self.query).order_by('id')
=======

    def get_queryset(self):
        queryset = self.model.objects.all()
        status = self.request.GET.get('status', '').strip()

        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            queryset = queryset.filter(activo=True)
        elif status == 'inactive':
            queryset = queryset.filter(activo=False)

        return queryset.order_by('id')
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_horario_atencion'] = reverse_lazy('doctor:horario_atencion_create')
<<<<<<< HEAD
        
        
        
        return context


class HorarioAtencionCreateView(CreateView):
    ...

class HorarioAtencionUpdateView(UpdateView):
    ...

class HorarioAtencionDeleteView(DeleteView):
    ...
=======
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
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
