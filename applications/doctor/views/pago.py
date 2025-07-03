from django.http import JsonResponse
<<<<<<< HEAD
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q, Sum
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    Pago, DetallePago, ServiciosAdicionales
    )
import json
=======
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    Pago
    )
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6


#VISTAS DE EMPLEADO

<<<<<<< HEAD
class PagoListView(PermissionRequiredMixin, ListView):
    model = Pago
    template_name = 'doctor/pago/pagolistview.html'
    context_object_name = 'pagos'
=======
class PagoListView(ListView):
    model = Pago
    template_name = 'doctor/pago/pagolistview.html'
    context_object_name = 'pago'
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
    permission_required = 'view_pago'
    

    def get_queryset(self):
<<<<<<< HEAD
        # Iniciar con la consulta base
        queryset = Pago.objects.select_related('atencion__paciente').prefetch_related('detalles').all()
        
        
        # Filtrar existente
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        metodo = self.request.GET.get('metodo')
        
        if q:
            queryset = queryset.filter(
                Q(atencion__paciente__nombres__icontains=q) |
                Q(atencion__paciente__apellidos__icontains=q) |
                Q(nombre_pagador__icontains=q) |
                Q(observaciones__icontains=q)
            )
        
        if status:
            queryset = queryset.filter(estado=status)
            
        if metodo:
            queryset = queryset.filter(metodo_pago=metodo)
        
        return queryset.order_by('-fecha_creacion')
=======
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        
        
        # Filtrar por estado (activo/inactivo)
        return queryset.filter(self.query).order_by('id')
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_pago'] = reverse_lazy('doctor:pago_create')
        
<<<<<<< HEAD
        # Estadísticas
        context['total_pendiente'] = Pago.objects.filter(estado='pendiente').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
        context['total_pagado'] = Pago.objects.filter(estado='pagado').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
=======
        
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
        
        return context


<<<<<<< HEAD
class PagoFacturacionView(PermissionRequiredMixin, View):
    """Vista principal de facturación"""
    permission_required = 'doctor.change_pago'
    
    def get(self, request, pk):
        pago = get_object_or_404(Pago, pk=pk)
        servicios_disponibles = ServiciosAdicionales.objects.filter(activo=True).order_by('nombre_servicio')
        
        context = {
            'pago': pago,
            'servicios_disponibles': servicios_disponibles,
            'paypal_client_id': 'sb',  # Cambiar por tu client ID real
        }
        
        return render(request, 'doctor/pago/pago_facturacion.html', context)
    
    def post(self, request, pk):
        """Procesar datos de facturación usando DetallePago"""
        pago = get_object_or_404(Pago, pk=pk)
        
        try:
            # Actualizar información del pago
            pago.nombre_pagador = request.POST.get('nombre_pagador', '')
            pago.observaciones = request.POST.get('observaciones', '')
            
            # Procesar servicios agregados
            servicios_data = json.loads(request.POST.get('servicios_json', '[]'))
            
            # Limpiar detalles existentes
            pago.detalles.all().delete()
            
            # Crear nuevos detalles usando tu modelo DetallePago
            total = 0
            for servicio_data in servicios_data:
                servicio = ServiciosAdicionales.objects.get(id=servicio_data['servicio_id'])
                
                detalle = DetallePago.objects.create(
                    pago=pago,
                    servicio_adicional=servicio,
                    cantidad=servicio_data['cantidad'],
                    precio_unitario=servicio.costo_servicio,
                    descuento_porcentaje=servicio_data.get('descuento', 0),
                    aplica_seguro=servicio_data.get('aplica_seguro', False),
                    valor_seguro=servicio_data.get('valor_seguro') if servicio_data.get('aplica_seguro') else None,
                    descripcion_seguro=servicio_data.get('descripcion_seguro', '')
                )
                # El subtotal se calcula automáticamente en tu modelo DetallePago
                total += detalle.subtotal
            
            # Actualizar total del pago
            pago.monto_total = total
            pago.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Facturación actualizada correctamente',
                'total': float(total)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

class PagoProcesarPagoView(PermissionRequiredMixin, View):
    """Vista para procesar el pago final"""
    permission_required = 'doctor.change_pago'
    
    def post(self, request, pk):
        pago = get_object_or_404(Pago, pk=pk)
        metodo_pago = request.POST.get('metodo_pago')
        
        if metodo_pago == 'efectivo':
            # Pago en efectivo
            pago.estado = 'pagado'
            pago.metodo_pago = 'efectivo'
            pago.fecha_pago = timezone.now()
            pago.save()
            
            messages.success(request, 'Pago en efectivo registrado exitosamente')
            
            return JsonResponse({
                'success': True,
                'message': 'Pago registrado exitosamente',
                'redirect_url': reverse('doctor:pago_detail', kwargs={'pk': pago.pk})
            })
            
        elif metodo_pago == 'paypal':
            # PayPal - preparar para pago
            pago.metodo_pago = 'paypal'
            pago.estado = 'pendiente'
            pago.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Preparado para pago con PayPal',
                'paypal_ready': True
            })
        
        return JsonResponse({
            'success': False,
            'error': 'Método de pago no válido'
        }, status=400)

class PayPalConfirmView(PermissionRequiredMixin, View):
    """Confirmar pago de PayPal"""
    permission_required = 'change_pago'
    
    def post(self, request, pk):
        pago = get_object_or_404(Pago, pk=pk)
        paypal_order_id = request.POST.get('paypal_order_id')
        paypal_transaction_id = request.POST.get('paypal_transaction_id', '')
        
        if paypal_order_id:
            pago.estado = 'pagado'
            pago.paypal_order_id = paypal_order_id  # Nuevo campo
            pago.referencia_externa = paypal_transaction_id  # Campo existente
            pago.fecha_pago = timezone.now()
            pago.save()
            
            messages.success(request, '¡Pago con PayPal completado exitosamente!')
            
            return JsonResponse({
                'success': True,
                'message': 'Pago completado exitosamente',
                'redirect_url': reverse('doctor:pago_detail', kwargs={'pk': pago.pk})
            })
        
        return JsonResponse({
            'success': False,
            'error': 'No se recibió confirmación de PayPal'
        }, status=400)
        


class PagoDetailView(PermissionRequiredMixin, View):
    """Vista de detalle del pago"""
    permission_required = 'view_pago'
    
    def get(self, request, pk):
        pago = get_object_or_404(Pago, pk=pk)
        
        context = {
            'pago': pago,
            'detalles': pago.detalles.select_related('servicio_adicional').all()
        }
        
        return render(request, 'doctor/pago/pago_detail.html', context)
    
    
class PagoDeleteView(PermissionRequiredMixin, DeleteView):
=======
class PagoCreateView(CreateView):
    ...

class PagoUpdateView(UpdateView):
    ...

class PagoDeleteView(DeleteView):
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
    ...