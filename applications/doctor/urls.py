from django.urls import path

from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView

from applications.doctor.views.cita_medica import (
    CitaMedicaListView, CitaMedicaCreateView, CitaMedicaDeleteView, CitaMedicaUpdateView
)

from applications.doctor.views.horario_atencion import (
    HorarioAtencionListView, HorarioAtencionCreateView, HorarioAtencionDeleteView, HorarioAtencionUpdateView
)

from applications.doctor.views.pago import (
    PagoListView, PagoCreateView, PagoDeleteView, PagoUpdateView
)

from applications.doctor.views.servicios_adicionales import (
    ServiciosAdicionalesListView, ServiciosAdicionalesCreateView, ServiciosAdicionalesDeleteView, ServiciosAdicionalesUpdateView
)


app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),

    # Rutas CITA MEDICA
    path('citas_list/', CitaMedicaListView.as_view(), name="cita_medica_list"),
    path('citas_create/', CitaMedicaCreateView.as_view(), name="cita_medica_create"),
    path('citas_update/<int:pk>/', CitaMedicaDeleteView.as_view(), name="cita_medica_update"),
    path('citas_delete/<int:pk>/', CitaMedicaUpdateView.as_view(), name="cita_medica_delete"),

    # Rutas HORARIO ATENCION
    path('horario_atencion_list/', HorarioAtencionListView.as_view(), name="horario_atencion_list"),
    path('horario_atencion_create/', HorarioAtencionCreateView.as_view(), name="horario_atencion_create"),
    path('horario_atencion_update/<int:pk>/', HorarioAtencionDeleteView.as_view(), name="horario_atencion_update"),
    path('horario_atencion_delete/<int:pk>/', HorarioAtencionUpdateView.as_view(), name="horario_atencion_delete"),

    # Rutas  PAGO
    path('pago_list/', PagoListView.as_view(), name="pago_list"),
    path('pago_create/', PagoCreateView.as_view(), name="pago_create"),
    path('pago_update/<int:pk>/', PagoDeleteView.as_view(), name="pago_update"),
    path('pago_delete/<int:pk>/', PagoUpdateView.as_view(), name="pago_delete"),


    # Rutas  SERVICIOS ADICIONALES
    path('servicio_adicional_list/', ServiciosAdicionalesListView.as_view(), name="servicios_adicionales_list"),
    path('servicio_adicional_create/', ServiciosAdicionalesCreateView.as_view(), name="servicios_adicionales_create"),
    path('servicio_adicional_update/<int:pk>/', ServiciosAdicionalesDeleteView.as_view(), name="servicios_adicionales_update"),
    path('servicio_adicional_delete/<int:pk>/', ServiciosAdicionalesUpdateView.as_view(), name="servicios_adicionales_delete"),

]