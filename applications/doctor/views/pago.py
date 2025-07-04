from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from applications.doctor.forms.pago import PagoForm
from django.db.models import Q, Sum
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView
from applications.doctor.models import (
    Pago, DetallePago, ServiciosAdicionales
)
import json



#VISTAS DE EMPLEADO


class PagoListView(PermissionRequiredMixin, ListView):
    model = Pago
    template_name = 'doctor/pago/pagolistview.html'
    context_object_name = 'pagos'
    permission_required = 'view_pago'
    
    def get_queryset(self):
        # Consulta base sin campos que pueden no existir
        queryset = Pago.objects.select_related('atencion__paciente').prefetch_related('detalles').all()
        
        # Filtros
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        metodo = self.request.GET.get('metodo')
        
        if q:
            # Filtrar sin usar campos que pueden no existir
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_pago'] = reverse_lazy('doctor:pago_create')
        
        # Estadísticas
        context['total_pendiente'] = Pago.objects.filter(estado='pendiente').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
        context['total_pagado'] = Pago.objects.filter(estado='pagado').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
        
        return context



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
    permission_required = 'doctor.change_pago'

    def post(self, request, pk):
        pago = get_object_or_404(Pago, pk=pk)
        metodo_pago = request.POST.get('metodo_pago')

        try:
            if metodo_pago == 'efectivo':
                pago.estado = 'pagado'
                pago.metodo_pago = 'efectivo'
                pago.fecha_pago = timezone.now()
                pago.save()
                messages.success(request, '¡Pago en efectivo registrado exitosamente!')
                return redirect('doctor:pago_detail', pk=pago.pk)

            elif metodo_pago == 'transferencia':
                pago.metodo_pago = 'transferencia'
                pago.estado = 'pagado'
                pago.fecha_pago = timezone.now()
                
                # Procesar evidencia de pago
                if 'evidencia_pago' in request.FILES:
                    pago.evidencia_pago = request.FILES['evidencia_pago']
                
                pago.save()
                messages.success(request, '¡Pago por transferencia registrado exitosamente!')
                return redirect('doctor:pago_detail', pk=pago.pk)

            elif metodo_pago == 'paypal':
                # PayPal se procesa via AJAX, no debería llegar aquí
                messages.info(request, 'Procesando pago con PayPal...')
                return redirect('doctor:pago_facturacion', pk=pago.pk)

            else:
                messages.error(request, 'Método de pago no válido')
                return redirect('doctor:pago_facturacion', pk=pago.pk)
                
        except Exception as e:
            messages.error(request, f'Error al procesar el pago: {str(e)}')
            return redirect('doctor:pago_facturacion', pk=pago.pk)
        
# Reemplaza tu PayPalConfirmView con esta versión:

class PayPalConfirmView(PermissionRequiredMixin, View):
    """Confirmar pago de PayPal"""
    permission_required = 'change_pago'
    
    def post(self, request, pk):
        pago = get_object_or_404(Pago, pk=pk)
        paypal_order_id = request.POST.get('paypal_order_id')
        paypal_transaction_id = request.POST.get('paypal_transaction_id', '')
        
        try:
            if paypal_order_id:
                pago.estado = 'pagado'
                pago.metodo_pago = 'paypal'
                pago.fecha_pago = timezone.now()
                
                # Usar el campo existente referencia_externa para guardar ambas referencias
                pago.set_paypal_references(paypal_order_id, paypal_transaction_id)
                pago.save()
                
                messages.success(request, '¡Pago con PayPal completado exitosamente!')
                
                return JsonResponse({
                    'success': True,
                    'message': 'Pago completado exitosamente',
                    'redirect_url': reverse('doctor:pago_detail', kwargs={'pk': pago.pk})
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No se recibió confirmación de PayPal'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar el pago: {str(e)}'
            }, status=500)
            
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
    

class PagoCreateView(PermissionRequiredMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pago/pago_create.html'
    permission_required = 'doctor.add_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = ServiciosAdicionales.objects.filter(activo=True).order_by('nombre_servicio')
        # Verificar qué campos están disponibles
        context['has_paciente_field'] = hasattr(Pago, 'paciente')
        context['has_monto_consulta_field'] = hasattr(Pago, 'monto_consulta')
        return context

    def form_valid(self, form):
        # Crear el pago como pendiente
        form.instance.estado = 'pendiente'
        form.instance.monto_total = 0
        pago = form.save()
        
        # Obtener monto de consulta si existe
        monto_consulta = 0
        if hasattr(Pago, 'monto_consulta'):
            monto_consulta = float(form.cleaned_data.get('monto_consulta') or 0)
        
        # Procesar servicios del formulario
        servicios_ids = self.request.POST.getlist('servicio_id[]')
        cantidades = self.request.POST.getlist('cantidad[]')
        descuentos = self.request.POST.getlist('descuento[]')
        
        total_servicios = 0
        for i, servicio_id in enumerate(servicios_ids):
            if servicio_id:
                servicio = ServiciosAdicionales.objects.get(id=servicio_id)
                cantidad = int(cantidades[i]) if i < len(cantidades) else 1
                descuento = float(descuentos[i]) if i < len(descuentos) else 0
                
                detalle = DetallePago.objects.create(
                    pago=pago,
                    servicio_adicional=servicio,
                    cantidad=cantidad,
                    precio_unitario=servicio.costo_servicio,
                    descuento_porcentaje=descuento
                )
                total_servicios += float(detalle.subtotal)
        
        # Actualizar el total del pago
        total_final = monto_consulta + total_servicios
        pago.monto_total = total_final
        
        # Guardar monto_consulta si existe el campo
        if hasattr(pago, 'monto_consulta'):
            pago.monto_consulta = monto_consulta
        
        pago.save()
        
        messages.success(self.request, f'Factura creada exitosamente por ${total_final:.2f}')
        return redirect('doctor:pago_facturacion', pk=pago.pk)