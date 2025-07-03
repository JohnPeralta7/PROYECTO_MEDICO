from django.urls import path
from applications.core.views.paciente import (
    paciente_find, PacienteListView, PacienteCreateView, PacienteDeleteView, PacienteUpdateView
    )
from applications.core.views.medicamento import (
     MedicamentoListView, MedicamentoCreateView, MedicamentoDeleteView, MedicamentoUpdateView,
     crear_tipo_medicamento_ajax, crear_marca_medicamento_ajax, recargar_tipos_marcas_medicamento,
     eliminar_medicamento_ajax

    )
from applications.core.views.gasto_mensual import (
     GastoMensualListView, GastoMensualCreateView, GastoMensualDeleteView, GastoMensualUpdateView
    )
from applications.core.views.empleado import (
     EmpleadoListView, EmpleadoCreateView, EmpleadoDeleteView, EmpleadoUpdateView
    )
from applications.core.views.doctor import (
     DoctorListView, DoctorCreateView, DoctorDeleteView, DoctorUpdateView
    )
from applications.core.views.diagnostico import (
     DiagnosticoListView, DiagnosticoCreateView, DiagnosticoDeleteView, DiagnosticoUpdateView
    )
from applications.core.views.paciente import paciente_json

app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Pacientes
    path('paciente_find/', paciente_find, name="paciente_find"),
    path('paciente_list/', PacienteListView.as_view(), name='paciente_list'),
    path('paciente_create/', PacienteCreateView.as_view(), name='paciente_create'),
    path('paciente_delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    path('paciente_update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('paciente/<int:pk>/json/', paciente_json, name='paciente_json'),



    #RUTAS DE MEDICAMENTO
    #path('paciente_find/', paciente_find, name="paciente_find"), por si deseas crear una autocompletacion como en pacientes
    path('medicamentos_list/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos_create/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos_delete/<int:pk>/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),

    path('medicamentos_delete_ajax/<int:pk>/', eliminar_medicamento_ajax, name='medicamento_delete_ajax'),
    path('medicamentos_update/<int:pk>/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('crear_tipo_medicamento/', crear_tipo_medicamento_ajax, name='crear_tipo_medicamento'),
    path('crear_marca_medicamento/', crear_marca_medicamento_ajax, name='crear_marca_medicamento'),
    path('recargar_tipos_marcas/', recargar_tipos_marcas_medicamento, name='recargar_tipos_marcas'),


    #RUTAS DE Gasto Mensual
    #path('gasto_mensual_find/', paciente_find, name="paciente_find"),
    path('gastos_mensual_list/', GastoMensualListView.as_view(), name='gasto_mensual_list'),
    path('gastos_mensual_create/', GastoMensualCreateView.as_view(), name='gasto_mensual_create'),
    path('gastos_mensual_delete/<int:pk>/', GastoMensualDeleteView.as_view(), name='gasto_mensual_delete'),
    path('gastos_mensual_update/<int:pk>/', GastoMensualUpdateView.as_view(), name='gasto_mensual_update'),


    #RUTAS DE EMPLEADO
    #path('p_find/', paciente_find, name="paciente_find"),
    path('empleado_list/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado_create/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado_delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
    path('empleado_update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),


    #RUTAS DE DOCTOR
    #path('p_find/', paciente_find, name="paciente_find"),
    path('doctor_list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor_create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor_delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('doctor_update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),


    #RUTAS DE DIAGNOSTICO
    #path('paciente_find/', paciente_find, name="paciente_find"),
    path('diagnostico_list/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnostico_create/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnostico_delete/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),
    path('diagnostico_update/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),

]
#tengo que hacer 