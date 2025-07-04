from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, date
from calendar import monthrange
from collections import defaultdict

from applications.doctor.models import CitaMedica, HorarioAtencion
from applications.core.models import Paciente


class CalendarioCitasView(TemplateView):
    """Vista principal del calendario de citas"""
    template_name = 'doctor/cita_medica/cita_medicalistview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener año y mes de los parámetros GET o usar el actual
        today = timezone.now().date()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        
        # Validar año y mes
        if year < 2020 or year > 2030:
            year = today.year
        if month < 1 or month > 12:
            month = today.month
            
        # Crear fecha del primer día del mes
        first_day = date(year, month, 1)
        
        # Obtener información del calendario
        calendar_data = self._generate_calendar_data(year, month)
        
        context.update({
            'year': year,
            'month': month,
            'month_name': first_day.strftime('%B'),
            'calendar_data': calendar_data,
            'today': today,
            'prev_month': self._get_prev_month(year, month),
            'next_month': self._get_next_month(year, month),
            'pacientes': Paciente.objects.filter(activo=True).order_by('nombres'),
            'create_cita_medica': reverse_lazy('doctor:cita_medica_create'),
        })
        
        return context
    
    def _generate_calendar_data(self, year, month):
        """Genera los datos del calendario con disponibilidad"""
        # Obtener el primer y último día del mes
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Obtener todas las citas del mes
        citas_mes = CitaMedica.objects.filter(
            fecha__gte=first_day,
            fecha__lte=last_day
        ).select_related('paciente')
        
        # Agrupar citas por fecha
        citas_por_fecha = defaultdict(list)
        for cita in citas_mes:
            citas_por_fecha[cita.fecha].append(cita)
        
        # Obtener horarios de atención por día
        horarios_atencion = {}
        for horario in HorarioAtencion.objects.filter(activo=True):
            dia_num = self._get_weekday_number(horario.dia_semana)
            horarios_atencion[dia_num] = horario
        
        # Generar datos del calendario
        calendar_days = []
        
        # Obtener el primer lunes de la semana que contiene el primer día del mes
        start_date = first_day - timedelta(days=first_day.weekday())
        
        # Generar 6 semanas (42 días) para cubrir todo el mes
        for i in range(42):
            current_date = start_date + timedelta(days=i)
            
            # Verificar si este día tiene horario de atención
            weekday = current_date.weekday()
            horario = horarios_atencion.get(weekday)
            
            # Obtener citas de este día
            citas_dia = citas_por_fecha.get(current_date, [])
            
            # Generar horarios disponibles si hay horario de atención
            horarios_disponibles = []
            horarios_ocupados = []
            
            if horario:
                horarios_disponibles, horarios_ocupados = self._generate_day_schedule(
                    horario, citas_dia
                )
            
            day_data = {
                'date': current_date,
                'is_current_month': current_date.month == month,
                'is_today': current_date == timezone.now().date(),
                'is_past': current_date < timezone.now().date(),
                'has_schedule': bool(horario),
                'horarios_disponibles': horarios_disponibles,
                'horarios_ocupados': horarios_ocupados,
                'citas': citas_dia,
                'total_citas': len(citas_dia)
            }
            
            calendar_days.append(day_data)
        
        return calendar_days
    
    def _generate_day_schedule(self, horario, citas_dia):
        """Genera los horarios disponibles y ocupados para un día específico"""
        horarios_disponibles = []
        horarios_ocupados = []
        
        # Crear lista de horarios cada 30 minutos
        current_time = datetime.combine(date.today(), horario.hora_inicio)
        end_time = datetime.combine(date.today(), horario.hora_fin)
        
        # Obtener las horas de las citas ocupadas
        horas_ocupadas = {cita.hora_cita for cita in citas_dia}
        
        while current_time.time() < end_time.time():
            # Verificar si está en el intervalo de descanso
            if (horario.intervalo_desde and horario.intervalo_hasta and 
                horario.intervalo_desde <= current_time.time() <= horario.intervalo_hasta):
                current_time += timedelta(minutes=30)
                continue
            
            # Verificar si esta hora está ocupada
            if current_time.time() in horas_ocupadas:
                horarios_ocupados.append(current_time.time())
            else:
                horarios_disponibles.append(current_time.time())
            
            current_time += timedelta(minutes=30)
        
        return horarios_disponibles, horarios_ocupados
    
    def _get_weekday_number(self, dia_semana):
        """Convierte el nombre del día a número de semana (0=lunes, 6=domingo)"""
        dias = {
            'lunes': 0,
            'martes': 1,
            'miércoles': 2,
            'jueves': 3,
            'viernes': 4,
            'sábado': 5,
            'domingo': 6
        }
        return dias.get(dia_semana.lower(), 0)
    
    def _get_prev_month(self, year, month):
        """Obtiene el año y mes anterior"""
        if month == 1:
            return {'year': year - 1, 'month': 12}
        return {'year': year, 'month': month - 1}
    
    def _get_next_month(self, year, month):
        """Obtiene el año y mes siguiente"""
        if month == 12:
            return {'year': year + 1, 'month': 1}
        return {'year': year, 'month': month + 1}


class CitaMedicaListView(CalendarioCitasView):
    """Vista principal que muestra el calendario de citas (heredando de CalendarioCitasView)"""
    pass


@login_required
@require_http_methods(["GET"])
def get_day_schedule_ajax(request):
    """Vista AJAX para obtener los horarios de un día específico"""
    fecha_str = request.GET.get('fecha')
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Fecha inválida'}, status=400)
    
    # Obtener el día de la semana
    weekday = fecha.weekday()
    
    # Buscar horario de atención para este día
    horario = HorarioAtencion.objects.filter(
        activo=True,
        dia_semana__in=[
            'lunes', 'martes', 'miércoles', 'jueves', 
            'viernes', 'sábado', 'domingo'
        ]
    ).first()
    
    if not horario:
        return JsonResponse({
            'fecha': fecha_str,
            'has_schedule': False,
            'horarios_disponibles': [],
            'horarios_ocupados': [],
            'message': 'No hay horario de atención configurado para este día'
        })
    
    # Obtener citas existentes para esta fecha
    citas_dia = CitaMedica.objects.filter(fecha=fecha).select_related('paciente')
    
    # Generar horarios
    calendar_view = CalendarioCitasView()
    horarios_disponibles, horarios_ocupados = calendar_view._generate_day_schedule(
        horario, citas_dia
    )
    
    # Convertir times a strings para JSON
    horarios_disponibles_str = [h.strftime('%H:%M') for h in horarios_disponibles]
    horarios_ocupados_str = [h.strftime('%H:%M') for h in horarios_ocupados]
    
    # Información de las citas existentes
    citas_info = []
    for cita in citas_dia:
        citas_info.append({
            'id': cita.id,
            'paciente': cita.paciente.nombre_completo,
            'hora': cita.hora_cita.strftime('%H:%M'),
            'estado': cita.estado,
            'observaciones': cita.observaciones or ''
        })
    
    return JsonResponse({
        'fecha': fecha_str,
        'has_schedule': True,
        'horarios_disponibles': horarios_disponibles_str,
        'horarios_ocupados': horarios_ocupados_str,
        'citas': citas_info
    })


@login_required
@require_http_methods(["POST"])
def crear_cita_ajax(request):
    """Vista AJAX para crear una nueva cita"""
    fecha_str = request.POST.get('fecha')
    hora_str = request.POST.get('hora')
    paciente_id = request.POST.get('paciente_id')
    observaciones = request.POST.get('observaciones', '')
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        paciente = get_object_or_404(Paciente, id=paciente_id)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Datos inválidos'}, status=400)
    
    # Verificar que no existe una cita en esta fecha y hora
    if CitaMedica.objects.filter(fecha=fecha, hora_cita=hora).exists():
        return JsonResponse({'error': 'Ya existe una cita en esta fecha y hora'}, status=400)
    
    # Verificar que la fecha no sea en el pasado
    if fecha < timezone.now().date():
        return JsonResponse({'error': 'No se pueden crear citas en fechas pasadas'}, status=400)
    
    # Crear la cita
    cita = CitaMedica.objects.create(
        paciente=paciente,
        fecha=fecha,
        hora_cita=hora,
        estado='disponible',  # Estado inicial
        observaciones=observaciones
    )
    
    return JsonResponse({
        'success': True,
        'message': f'Cita creada exitosamente para {paciente.nombre_completo}',
        'cita': {
            'id': cita.id,
            'paciente': cita.paciente.nombre_completo,
            'fecha': cita.fecha.strftime('%Y-%m-%d'),
            'hora': cita.hora_cita.strftime('%H:%M'),
            'estado': cita.estado,
            'observaciones': cita.observaciones or ''
        }
    })


class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/cita_medica_create.html'
    fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
    success_url = reverse_lazy('doctor:cita_medica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cita médica creada exitosamente.')
        return super().form_valid(form)


class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/cita_medica_update.html'
    fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
    success_url = reverse_lazy('doctor:cita_medica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cita médica actualizada exitosamente.')
        return super().form_valid(form)


class CitaMedicaDeleteView(DeleteView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/cita_medica_delete.html'
    success_url = reverse_lazy('doctor:cita_medica_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cita médica eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
    
