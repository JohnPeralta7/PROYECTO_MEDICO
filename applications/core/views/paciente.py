from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from applications.core.forms.paciente import PacienteForm
from applications.core.models import Paciente
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from applications.core.models import (
    Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
    )

"""  Vista para buscar pacientes mediante AJAX. Por nombres, apellidos, cédula o teléfono. """


@login_required
@require_http_methods(["GET"])
def paciente_find(request):
    try:
        # Obtener el parámetro de búsqueda
        query = request.GET.get('q', '').strip()

        # Validar que se proporcione al menos 3 caracteres
        if len(query) < 3:
            return JsonResponse({
                'success': False,
                'message': 'Debe proporcionar al menos 3 caracteres para la búsqueda',
                'pacientes': []
            })

        # Construir la consulta de búsqueda
        # Buscar en nombres, apellidos, cédula, DNI y teléfono
        pacientes_query = Paciente.objects.filter(
            Q(activo=True) & (
                    Q(nombres__icontains=query) |
                    Q(apellidos__icontains=query) |
                    Q(cedula_ecuatoriana__icontains=query) |
                    Q(dni__icontains=query) |
                    Q(telefono__icontains=query)
            )
        ).select_related('tipo_sangre').prefetch_related(
            'atenciones__diagnostico',
            'atenciones__detalles__medicamento'
        ).order_by('apellidos', 'nombres')

        # Limitar resultados para mejorar rendimiento
        pacientes_query = pacientes_query[:20]

        # Convertir a lista de diccionarios
        pacientes_data = []
        for paciente in pacientes_query:
            # Calcular edad
            edad = paciente.edad

            # Obtener atenciones anteriores (últimas 10)
            atenciones = []
            for atencion in paciente.atenciones.all()[:10]:
                # Obtener prescripciones/detalles de esta atención
                detalles = []
                for detalle in atencion.detalles.all():
                    detalle_dict = {
                        'medicamento': detalle.medicamento.nombre if detalle.medicamento else None,
                        'cantidad': detalle.cantidad,
                        'prescripcion': detalle.prescripcion,
                        'duracion_tratamiento': detalle.duracion_tratamiento,
                        'frecuencia_diaria': detalle.frecuencia_diaria,
                    }
                    detalles.append(detalle_dict)

                # Obtener diagnósticos
                diagnosticos = [d.descripcion for d in atencion.diagnostico.all()]

                # Determinar tipo de consulta
                tipo_consulta = "Chequeo"
                if atencion.es_control:
                    tipo_consulta = "Control"
                elif "urgencia" in atencion.motivo_consulta.lower() or "dolor" in atencion.motivo_consulta.lower():
                    tipo_consulta = "Urgencia"

                atencion_dict = {
                    'id': atencion.id,
                    'fecha_atencion': atencion.fecha_atencion.isoformat(),
                    'tipo_consulta': tipo_consulta,

                    # Signos vitales
                    'presion_arterial': atencion.presion_arterial,
                    'pulso': atencion.pulso,
                    'temperatura': float(atencion.temperatura) if atencion.temperatura else None,
                    'frecuencia_respiratoria': atencion.frecuencia_respiratoria,
                    'saturacion_oxigeno': float(atencion.saturacion_oxigeno) if atencion.saturacion_oxigeno else None,
                    'peso': float(atencion.peso) if atencion.peso else None,
                    'altura': float(atencion.altura) if atencion.altura else None,
                    'imc': atencion.calcular_imc,

                    # Contenido de la atención
                    'motivo_consulta': atencion.motivo_consulta,
                    'sintomas': atencion.sintomas,
                    'tratamiento': atencion.tratamiento,
                    'diagnosticos': diagnosticos,
                    'examen_fisico': atencion.examen_fisico,
                    'examenes_enviados': atencion.examenes_enviados,
                    'comentario_adicional': atencion.comentario_adicional,
                    'es_control': atencion.es_control,

                    # Prescripciones
                    'prescripciones': detalles
                }
                atenciones.append(atencion_dict)

            paciente_dict = {
                'id': paciente.id,
                'nombres': paciente.nombres,
                'apellidos': paciente.apellidos,
                'cedula_ecuatoriana': paciente.cedula_ecuatoriana,
                'dni': paciente.dni,
                'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                'edad': edad,
                'telefono': paciente.telefono,
                'email': paciente.email,
                'sexo': paciente.sexo,
                'estado_civil': paciente.estado_civil,
                'direccion': paciente.direccion,
                'latitud': float(paciente.latitud) if paciente.latitud else None,
                'longitud': float(paciente.longitud) if paciente.longitud else None,
                'tipo_sangre': paciente.tipo_sangre.tipo if paciente.tipo_sangre else None,
                'foto_url': paciente.get_image,

                # Historia clínica
                'antecedentes_personales': paciente.antecedentes_personales,
                'antecedentes_quirurgicos': paciente.antecedentes_quirurgicos,
                'antecedentes_familiares': paciente.antecedentes_familiares,
                'alergias': paciente.alergias,
                'medicamentos_actuales': paciente.medicamentos_actuales,
                'habitos_toxicos': paciente.habitos_toxicos,
                'vacunas': paciente.vacunas,
                'antecedentes_gineco_obstetricos': paciente.antecedentes_gineco_obstetricos,

                # Atenciones anteriores
                'atenciones': atenciones,
                'total_atenciones': paciente.atenciones.count()
            }
            pacientes_data.append(paciente_dict)
        print(pacientes_data)
        return JsonResponse({
            'success': True,
            'pacientes': pacientes_data,
            'total': len(pacientes_data),
            'query': query
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en la búsqueda: {str(e)}',
            'pacientes': []
        }, status=500)



class PacienteListView(PermissionMixin, ListViewMixin, ListView):
    model = Paciente
    template_name = 'core/paciente/pacientelistview.html'
    context_object_name = 'pacientes'
    permission_required = 'view_patient'
    

    def get_queryset(self):
        self.query = Q()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        # Iniciar con la consulta base
        queryset = self.model.objects.all()
        
        # Filtrar por término de búsqueda
        if q:
            self.query.add(Q(nombres__icontains=q) | 
                           Q(apellidos__icontains=q) | 
                           Q(cedula_ecuatoriana__icontains=q) | 
                           Q(dni__icontains=q) | 
                           Q(telefono__icontains=q), Q.AND)
        
        # Filtrar por estado (activo/inactivo)
        if status == 'active':
            self.query.add(Q(activo=True), Q.AND)
        elif status == 'inactive':
            self.query.add(Q(activo=False), Q.AND)
        
        return queryset.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_patient'] = reverse_lazy('core:paciente_create')
        
        # Agregamos estadísticas para el dashboard
        context['total_patient'] = Paciente.objects.count()
        context['active_patient'] = Paciente.objects.filter(activo=True).count()
        return context
    



class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar el paciente: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        paciente_name = f"{self.object.nombres} {self.object.apellidos}"
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el paciente {paciente_name}.")    
        return response



class PacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    template_name = 'core/paciente/pacienteupdate.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        personales = []
        clinico = []
        found = False
        for field in form.visible_fields():
            if field.name == "antecedentes_personales":
                found = True
            if not found:
                personales.append(field)
            else:
                clinico.append(field)
        context['personales'] = personales
        context['clinico'] = clinico
        return context

    def form_valid(self, form):
        paciente_name = f"{self.object.nombres} {self.object.apellidos}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al actualizar el paciente {paciente_name}.")
        return response


class PacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    template_name = 'core/paciente/pacientecreate.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        personales = []
        clinico = []
        found = False
        for field in form.visible_fields():
            if field.name == "antecedentes_personales":
                found = True
            if not found:
                personales.append(field)
            else:
                clinico.append(field)
        context['personales'] = personales
        context['clinico'] = clinico
        return context

    def form_valid(self, form):
        self.object = form.save()
        paciente_name = f"{self.object.nombres} {self.object.apellidos}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al crear el paciente {paciente_name}.")
        return response
    
    
@csrf_exempt  # Solo si tienes problemas de CSRF con fetch, si no, puedes quitarlo
def paciente_json(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    data = {
        "nombres": paciente.nombres or "",
        "apellidos": paciente.apellidos or "",
        "cedula_ecuatoriana": paciente.cedula_ecuatoriana or "",
        "dni": paciente.dni or "",
        "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d') if paciente.fecha_nacimiento else "",
        "telefono": paciente.telefono or "",
        "email": paciente.email or "",
        "sexo": paciente.sexo or "",
        "direccion": paciente.direccion or "",
        "estado_civil": paciente.estado_civil or "",
        "latitud": paciente.latitud or "",
        "longitud": paciente.longitud or "",
        # Cambia esta línea:
        "tipo_sangre": paciente.tipo_sangre.tipo if paciente.tipo_sangre else "",
        "foto": paciente.foto.url if getattr(paciente, "foto", None) and paciente.foto else "",
        "antecedentes_personales": paciente.antecedentes_personales or "",
        "antecedentes_familiares": paciente.antecedentes_familiares or "",
        "antecedentes_quirurgicos": paciente.antecedentes_quirurgicos or "",
        "alergias": paciente.alergias or "",
        "medicamentos_actuales": paciente.medicamentos_actuales or "",
        "habitos_toxicos": paciente.habitos_toxicos or "",
        "vacunas": paciente.vacunas or "",
        "antecedentes_gineco_obstetricos": paciente.antecedentes_gineco_obstetricos or "",
        "activo": paciente.activo,
    }
    return JsonResponse(data)


class PacienteCreateModalView(PacienteCreateView):
    """Vista que extiende PacienteCreateView para trabajar con AJAX desde modales"""
    
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch para manejar requests AJAX"""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return self.ajax_post(request)
        return super().dispatch(request, *args, **kwargs)
    
    def ajax_post(self, request):
        """Maneja requests POST via AJAX"""
        try:
            # Si los datos vienen como JSON
            if request.content_type == 'application/json':
                import json
                data = json.loads(request.body)
                form = self.form_class(data)
            else:
                # Si vienen como form-data
                form = self.form_class(request.POST, request.FILES)
            
            if form.is_valid():
                # Usar el método form_valid heredado que mantiene la lógica de permisos
                self.object = form.save()
                
                # Crear respuesta JSON con los datos del paciente
                paciente_data = self.get_paciente_json_data(self.object)
                
                return JsonResponse({
                    'success': True,
                    'message': f'Paciente {self.object.nombres} {self.object.apellidos} creado exitosamente',
                    'paciente': paciente_data
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Error en la validación del formulario',
                    'errors': form.errors
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error interno: {str(e)}'
            }, status=500)
    
    def get_paciente_json_data(self, paciente):
        """Convierte el paciente a formato JSON para la respuesta"""
        return {
            'id': paciente.id,
            'nombres': paciente.nombres,
            'apellidos': paciente.apellidos,
            'cedula_ecuatoriana': paciente.cedula_ecuatoriana,
            'dni': paciente.dni,
            'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
            'edad': paciente.edad,
            'telefono': paciente.telefono,
            'email': paciente.email,
            'sexo': paciente.sexo,
            'estado_civil': paciente.estado_civil,
            'direccion': paciente.direccion,
            'tipo_sangre': paciente.tipo_sangre.tipo if paciente.tipo_sangre else None,
            'foto_url': paciente.get_image,
            'antecedentes_personales': paciente.antecedentes_personales,
            'antecedentes_quirurgicos': paciente.antecedentes_quirurgicos,
            'antecedentes_familiares': paciente.antecedentes_familiares,
            'alergias': paciente.alergias,
            'medicamentos_actuales': paciente.medicamentos_actuales,
            'habitos_toxicos': paciente.habitos_toxicos,
            'vacunas': paciente.vacunas,
            'antecedentes_gineco_obstetricos': paciente.antecedentes_gineco_obstetricos,
            'atenciones': []
        }