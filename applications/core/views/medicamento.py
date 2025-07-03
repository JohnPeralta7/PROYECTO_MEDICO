from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual,
    TipoMedicamento, MarcaMedicamento
)
from applications.core.forms.medicamento import MedicamentoForm, MedicamentoBusquedaForm


#VISTAS DE MEDICAMENTO

class MedicamentoListView(PermissionRequiredMixin, ListView):
    model = Medicamento
    template_name = 'core/medicamento/medicamentolistview.html'
    context_object_name = 'medicamentos'
    permission_required = 'view_medicamento'
    paginate_by = 20
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        tipo = self.request.GET.get('tipo')
        marca = self.request.GET.get('marca')
        stock_minimo = self.request.GET.get('stock_minimo')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.select_related('tipo', 'marca_medicamento')
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(marca_medicamento__nombre__icontains=q) | 
                           Q(nombre__icontains=q) |
                           Q(tipo__nombre__icontains=q), Q.AND)
        
        # Filtrar por tipo
        if tipo:
            self.query.add(Q(tipo_id=tipo), Q.AND)
        
        # Filtrar por marca
        if marca:
            self.query.add(Q(marca_medicamento_id=marca), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(activo=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(activo=False), Q.AND)
        
        # Filtrar por stock mínimo
        if stock_minimo:
            try:
                stock_min = int(stock_minimo)
                self.query.add(Q(cantidad__gte=stock_min), Q.AND)
            except ValueError:
                pass
        
        return queryset.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:medicamento_create')
        context['search_form'] = MedicamentoBusquedaForm(self.request.GET or None)
        
        # Agregamos los tipos y marcas para el modal
        context['tipos_medicamento'] = TipoMedicamento.objects.filter(activo=True).order_by('nombre')
        context['marcas_medicamento'] = MarcaMedicamento.objects.filter(activo=True).order_by('nombre')
        
        # Agregamos estadísticas para el dashboard
        context['total_medicamentos'] = Medicamento.objects.count()
        context['active_medicamentos'] = Medicamento.objects.filter(activo=True).count()
        context['low_stock_medicamentos'] = Medicamento.objects.filter(cantidad__lt=10, activo=True).count()
        
        return context


class MedicamentoCreateView(PermissionRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/medicamento_form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'add_medicamento'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Medicamento'
        context['tipos_medicamento'] = TipoMedicamento.objects.filter(activo=True)
        context['marcas_medicamento'] = MarcaMedicamento.objects.filter(activo=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Medicamento "{form.instance.nombre}" creado exitosamente.')
        return super().form_valid(form)

class MedicamentoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/medicamento_form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'change_medicamento'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Medicamento'
        context['tipos_medicamento'] = TipoMedicamento.objects.filter(activo=True)
        context['marcas_medicamento'] = MarcaMedicamento.objects.filter(activo=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Medicamento "{form.instance.nombre}" actualizado exitosamente.')
        return super().form_valid(form)

class MedicamentoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Medicamento
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'delete_medicamento'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Medicamento'
        context['mensaje'] = f'¿Está seguro de eliminar el medicamento "{self.object.nombre}"?'
        return context

# Vista para mostrar el detalle de un medicamento
class MedicamentoDetailView(PermissionRequiredMixin, DetailView):
    model = Medicamento
    template_name = 'core/medicamento/medicamento_detail.html'
    context_object_name = 'medicamento'
    permission_required = 'view_medicamento'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalle: {self.object.nombre}'
        return context

# Vista AJAX para búsqueda rápida de medicamentos
@login_required
@require_http_methods(["GET"])
def medicamento_search_ajax(request):
    """
    Vista para búsqueda AJAX de medicamentos
    Útil para autocompletar en otros formularios
    """
    query = request.GET.get('q', '')
    medicamentos = []
    
    if query:
        medicamentos_qs = Medicamento.objects.filter(
            Q(nombre__icontains=query) |
            Q(marca_medicamento__nombre__icontains=query) |
            Q(tipo__nombre__icontains=query),
            activo=True
        ).select_related('tipo', 'marca_medicamento')[:10]  # Límite de 10 resultados
        
        medicamentos = [
            {
                'id': med.id,
                'nombre': med.nombre,
                'tipo': med.tipo.nombre,
                'marca': med.marca_medicamento.nombre if med.marca_medicamento else '',
                'precio': str(med.precio),
                'stock': med.cantidad,
                'concentracion': med.concentracion or '',
                'via_administracion': med.get_via_administracion_display()
            }
            for med in medicamentos_qs
        ]
    
    return JsonResponse({'medicamentos': medicamentos})

@csrf_exempt
def crear_tipo_medicamento_ajax(request):
    """
    Vista AJAX para crear un nuevo tipo de medicamento desde el modal
    """
    # Verificar que sea una petición POST
    if request.method != 'POST':
        return JsonResponse({
            'success': False, 
            'message': 'Método no permitido'
        })
    
    try:
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        # Debug - Imprimir datos recibidos
        print(f"Datos recibidos - Nombre: '{nombre}', Descripción: '{descripcion}'")
        print(f"Usuario: {request.user}")
        print(f"POST data: {request.POST}")
        
        # Validaciones
        if not nombre:
            return JsonResponse({
                'success': False,
                'message': 'El nombre del tipo es requerido.'
            })
        
        # Verificar si ya existe un tipo con ese nombre (case insensitive)
        if TipoMedicamento.objects.filter(nombre__iexact=nombre).exists():
            return JsonResponse({
                'success': False,
                'message': f'Ya existe un tipo de medicamento con el nombre "{nombre}".'
            })
        
        # Crear el nuevo tipo de medicamento
        nuevo_tipo = TipoMedicamento.objects.create(
            nombre=nombre.title(),  # Capitalizar primera letra
            descripcion=descripcion,
            activo=True
        )
        
        print(f"Tipo creado exitosamente: ID={nuevo_tipo.id}, Nombre={nuevo_tipo.nombre}")
        
        return JsonResponse({
            'success': True,
            'message': 'Tipo de medicamento creado exitosamente.',
            'tipo': {
                'id': nuevo_tipo.id,
                'nombre': nuevo_tipo.nombre,
                'descripcion': nuevo_tipo.descripcion or ''
            }
        })
        
    except Exception as e:
        import traceback
        print(f"Error en crear_tipo_medicamento_ajax: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        })

@csrf_exempt
def crear_marca_medicamento_ajax(request):
    """
    Vista AJAX para crear una nueva marca de medicamento desde el modal
    """
    # Verificar que sea una petición POST
    if request.method != 'POST':
        return JsonResponse({
            'success': False, 
            'message': 'Método no permitido'
        })
    
    try:
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        # Debug - Imprimir datos recibidos
        print(f"Datos recibidos - Nombre: '{nombre}', Descripción: '{descripcion}'")
        print(f"Usuario: {request.user}")
        print(f"POST data: {request.POST}")
        
        # Validaciones
        if not nombre:
            return JsonResponse({
                'success': False,
                'message': 'El nombre de la marca es requerido.'
            })
        
        # Verificar si ya existe una marca con ese nombre (case insensitive)
        if MarcaMedicamento.objects.filter(nombre__iexact=nombre).exists():
            return JsonResponse({
                'success': False,
                'message': f'Ya existe una marca de medicamento con el nombre "{nombre}".'
            })
        
        # Crear la nueva marca de medicamento
        nueva_marca = MarcaMedicamento.objects.create(
            nombre=nombre.title(),  # Capitalizar primera letra
            descripcion=descripcion,
            activo=True
        )
        
        print(f"Marca creada exitosamente: ID={nueva_marca.id}, Nombre={nueva_marca.nombre}")
        
        return JsonResponse({
            'success': True,
            'message': 'Marca de medicamento creada exitosamente.',
            'marca': {
                'id': nueva_marca.id,
                'nombre': nueva_marca.nombre,
                'descripcion': nueva_marca.descripcion or ''
            }
        })
        
    except Exception as e:
        import traceback
        print(f"Error en crear_marca_medicamento_ajax: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        })

@login_required
@require_http_methods(["GET"])
def recargar_tipos_marcas_medicamento(request):
    """
    Vista AJAX para recargar los tipos y marcas de medicamento en los selects
    """
    try:
        tipos = list(TipoMedicamento.objects.filter(activo=True).order_by('nombre').values('id', 'nombre'))
        marcas = list(MarcaMedicamento.objects.filter(activo=True).order_by('nombre').values('id', 'nombre'))
        
        return JsonResponse({
            'success': True,
            'tipos': tipos,
            'marcas': marcas
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al recargar datos: {str(e)}'
        })