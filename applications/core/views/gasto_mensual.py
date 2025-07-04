from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual, TipoGasto
    )
from applications.core.forms.gasto_mensual import GastoMensualForm, GastoMensualBusquedaForm


#VISTAS DE Gasto Mensual

class GastoMensualListView(PermissionRequiredMixin, ListView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/gasto_mensuallistview.html'
    context_object_name = 'gastos'
    permission_required = 'core.view_gastomensual'
    paginate_by = 10
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        tipo_gasto = self.request.GET.get('tipo_gasto')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.select_related('tipo_gasto').all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(tipo_gasto__nombre__icontains=q) | Q(observacion__icontains=q), Q.AND)
        
        # Filtrar por tipo de gasto
        if tipo_gasto:
            self.query.add(Q(tipo_gasto_id=tipo_gasto), Q.AND)
        
        # Filtrar por rango de fechas
        if fecha_desde:
            self.query.add(Q(fecha__gte=fecha_desde), Q.AND)
        if fecha_hasta:
            self.query.add(Q(fecha__lte=fecha_hasta), Q.AND)
        
        return queryset.filter(self.query).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:gasto_mensual_create')
        context['search_form'] = GastoMensualBusquedaForm(self.request.GET or None)
        
        # Agregamos estadísticas para el dashboard
        context['total_gastos'] = GastoMensual.objects.count()
        context['total_valor'] = GastoMensual.objects.aggregate(Sum('valor'))['valor__sum'] or 0
        context['tipos_gasto'] = TipoGasto.objects.filter(activo=True).order_by('nombre')
        
        return context


class GastoMensualCreateView(PermissionRequiredMixin, CreateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gasto_mensual/gasto_mensualcreate.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'core.add_gastomensual'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Gasto Mensual'
        context['tipos_gasto'] = TipoGasto.objects.filter(activo=True).order_by('nombre')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Gasto creado exitosamente'})
        messages.success(self.request, f'Gasto mensual "{form.instance.tipo_gasto}" creado exitosamente.')
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)


class GastoMensualUpdateView(PermissionRequiredMixin, UpdateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gasto_mensual/gasto_mensualcreate.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'core.change_gastomensual'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Gasto Mensual'
        context['tipos_gasto'] = TipoGasto.objects.filter(activo=True).order_by('nombre')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Gasto actualizado exitosamente'})
        messages.success(self.request, f'Gasto mensual "{form.instance.tipo_gasto}" actualizado exitosamente.')
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)


class GastoMensualDeleteView(PermissionRequiredMixin, DeleteView):
    model = GastoMensual
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'core.delete_gastomensual'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Gasto Mensual'
        context['mensaje'] = f'¿Está seguro de eliminar el gasto "{self.object.tipo_gasto}" del {self.object.fecha}?'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Gasto mensual eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


@login_required
@require_http_methods(["GET"])
def gasto_mensual_json(request):
    """
    Vista para obtener gastos mensuales en formato JSON
    """
    gastos = GastoMensual.objects.select_related('tipo_gasto').all()
    
    # Filtros
    q = request.GET.get('q')
    gasto_id = request.GET.get('id')
    
    if gasto_id:
        gastos = gastos.filter(id=gasto_id)
    elif q:
        gastos = gastos.filter(
            Q(tipo_gasto__nombre__icontains=q) | 
            Q(observacion__icontains=q)
        )
    
    data = []
    for gasto in gastos:
        data.append({
            'id': gasto.id,
            'tipo_gasto': gasto.tipo_gasto.nombre,
            'tipo_gasto_id': gasto.tipo_gasto.id,
            'fecha': gasto.fecha.strftime('%Y-%m-%d'),
            'valor': float(gasto.valor),
            'observacion': gasto.observacion or '',
        })
    
    return JsonResponse({'gastos': data})


@login_required
@require_http_methods(["GET"])
def gasto_mensual_chart_data(request):
    """
    Vista para obtener datos del gráfico de gastos mensuales
    """
    from django.db.models import Sum
    from django.db.models.functions import TruncMonth
    import json
    
    # Agrupar gastos por mes
    gastos_por_mes = GastoMensual.objects.annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total=Sum('valor')
    ).order_by('mes')
    
    # Preparar datos para el gráfico
    labels = []
    data = []
    
    for item in gastos_por_mes:
        labels.append(item['mes'].strftime('%B %Y'))
        data.append(float(item['total']))
    
    return JsonResponse({
        'labels': labels,
        'data': data
    })


@login_required
@require_http_methods(["POST"])
def tipo_gasto_create_ajax(request):
    """
    Vista AJAX para crear un nuevo tipo de gasto
    """
    try:
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if not nombre:
            return JsonResponse({
                'success': False,
                'message': 'El nombre del tipo de gasto es requerido'
            })
        
        # Verificar si ya existe un tipo de gasto con ese nombre
        if TipoGasto.objects.filter(nombre__iexact=nombre).exists():
            return JsonResponse({
                'success': False,
                'message': 'Ya existe un tipo de gasto con ese nombre'
            })
        
        # Crear el nuevo tipo de gasto
        tipo_gasto = TipoGasto.objects.create(
            nombre=nombre,
            descripcion=descripcion if descripcion else None,
            activo=True
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Tipo de gasto creado exitosamente',
            'tipo_gasto': {
                'id': tipo_gasto.id,
                'nombre': tipo_gasto.nombre,
                'descripcion': tipo_gasto.descripcion
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al crear el tipo de gasto: {str(e)}'
        })