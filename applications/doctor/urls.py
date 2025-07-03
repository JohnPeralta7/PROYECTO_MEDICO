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
    PagoListView, PagoFacturacionView, PagoProcesarPagoView, PayPalConfirmView, PagoDetailView
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
    path('citas_delete/<int:pk>/', CitaMedicaDeleteView.as_view(), name="cita_medica_delete"),
    path('citas_update/<int:pk>/', CitaMedicaUpdateView.as_view(), name="cita_medica_update"),


    # Rutas HORARIO ATENCION
    path('horario_atencion_list/', HorarioAtencionListView.as_view(), name="horario_atencion_list"),
    path('horario_atencion_create/', HorarioAtencionCreateView.as_view(), name="horario_atencion_create"),
    path('horario_atencion_delete/<int:pk>/', HorarioAtencionDeleteView.as_view(), name="horario_atencion_delete"),
    path('horario_atencion_update/<int:pk>/', HorarioAtencionUpdateView.as_view(), name="horario_atencion_update"),

    # Rutas  PAGO
    path('pago_list/', PagoListView.as_view(), name="pago_list"),
    path('pago_fact/', PagoFacturacionView.as_view(), name="pago_facturacion"),
    #path('pago_delete/<int:pk>/', PagoDeleteView.as_view(), name="pago_delete"),
    path('pago_/<int:pk>/', PagoProcesarPagoView.as_view(), name="pago_procesar_pago"),
    





    # Rutas  SERVICIOS ADICIONALES
    path('servicio_adicional_list/', ServiciosAdicionalesListView.as_view(), name="servicios_adicionales_list"),
    path('servicio_adicional_create/', ServiciosAdicionalesCreateView.as_view(), name="servicios_adicionales_create"),
    path('servicio_adicional_delete/<int:pk>/', ServiciosAdicionalesDeleteView.as_view(), name="servicios_adicionales_delete"),
    path('servicio_adicional_update/<int:pk>/', ServiciosAdicionalesUpdateView.as_view(), name="servicios_adicionales_update"),

]