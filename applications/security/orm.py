from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from applications.security.models import GroupModulePermission, Menu, Module, User

# Create Menus - using save() and create()
menu1 = Menu(
    name='Emergencia',
    icon='fa fa-person',
    order=7
)
menu1.save()

menu2 = Menu.objects.create(
    name='Consultas',
    icon='fa fa-calendar-check',
    order=2
)

menu3 = Menu.objects.create(
    name='Auditores',
    icon='fa fa-file',
    order=4
)

# Create Modules using bulk_create
modules = [
    
    Module(url='core/paciente_list/', name='Registro de Pacientes', menu_id=menu1.id,
           description='Gestión de información de pacientes', icon='fa fa-bed', order=1),
    Module(url='core/diagnostico_list/', name='Diagnostico', menu=menu1, 
           description='', icon='fa fa-stethoscope', order=2),
    Module(url='doctor/atencion_list/', name='Atencion', menu=menu1, 
           description='Aqui se llena los campos de receta para paciente', icon='fa fa-book', order=3),
    Module(url='doctor/horario_atencion_list/', name='Horario de Atencion', menu=menu1, 
           description='Se define el horario de trabajo del doctor', icon='fa fa-clock-o', order=4),
    Module(url='doctor/servicio_adicional_list/', name='Servicios Adicionales', menu=menu1, 
           description='Servicios como radiografias, eco, etc.', icon='fa fa-briefcase', order=5),       
           
    


    
    Module(url='doctor/citas_list/', name='Cita Medica', menu=menu2, 
           description='Programación de citas médicas', icon='fa fa-calendar', order=1),
    Module(url='core/gastos_mensual_list/', name='Gastos Mensual', menu=menu2, 
           description='Control de gastos varios del doctor', icon='fa fa-money-bill', order=2),
    Module(url='core/medicamentos_list/', name='Medicamentos', menu=menu2, 
           description='Medicamentos que puede recetar el doctor', icon='fa fa-heartbeat', order=3),
    Module(url='doctor/pago_list/', name='Pagos', menu=menu2, 
           description='Metodo de pago por Pay-Pal/efectivo/transferencia', icon='fa fa-credit-card', order=4),
    Module(url='core/doctor_list/', name='Doctores', menu=menu2, 
           description='Gestion de Doctores', icon='fa fa-user-md', order=5),
    Module(url='core/empleado_list/', name='Empleados', menu=menu2, 
           description='Gestion de Empleados', icon='fa fa-users', order=6),







    Module(url='configuracion/', name='Configuración', menu=menu3, 
           description='Configuración general del sistema', icon='fa fa-cog', order=2),
    Module(url='reportes/', name='Reportes', menu=menu3, 
           description='Generación de reportes y estadísticas', icon='fa fa-file-alt', order=3)
]

created_modules = Module.objects.bulk_create(modules)
module1, module2, module3, module4, module5, module6, module7, module8, module9, module10, module11, module12, module13 = created_modules

# Create Users
user1 = User.objects.create(
    username='dracandy',
    email='johnkaren@gmail.com',
    password='123',
    first_name='Candy',
    last_name='Peralta',
    dni='0912345678',
    direction='Av. Principal 123, Guayaquil',
    phone='0991234567',
    is_staff=True
)

user2 = User.objects.create(
    username='korochan',
    email='korochan@gmail.com',
    password='123',
    first_name='Korochan',
    last_name='Peralta',
    dni='0923456789',
    direction='Calle Secundaria 456, Guayaquil',
    phone='0982345678',
    is_staff=False
)

user3 = User.objects.create(
    username='Terry',
    email='terry@gmail.com',
    password='123',
    first_name='Terry',
    last_name='Peralta',
    dni='0923456789',
    direction='Calle Secundaria 456, Guayaquil',
    phone='0982345678',
    is_staff=False
)


# Create Groups
group_medicos = Group.objects.create(name='Médicos')
group_asistentes = Group.objects.create(name='Asistentes')
group_auditor = Group.objects.create(name='Auditor')

# Add users to groups y si se usa set() se eliminan los grupos anteriores
user1.groups.add(group_medicos)
user2.groups.add(group_asistentes)
user3.groups.add(group_auditor)


# Create permissions for Patient and Diagnosis models only
patient_ct = ContentType.objects.get(app_label='core', model='paciente')
diagnosis_ct = ContentType.objects.get(app_label='core', model='diagnostico')
doctor_ct = ContentType.objects.get(app_label='core', model='doctor')
empleados_ct = ContentType.objects.get(app_label='core', model='empleado')
medicamento_ct = ContentType.objects.get(app_label='core', model='medicamento')
gasto_mensual_ct = ContentType.objects.get(app_label='core', model='gastomensual')
horario_atencion_ct = ContentType.objects.get(app_label='doctor', model='horarioatencion')
cita_medica_ct = ContentType.objects.get(app_label='doctor', model='citamedica')
atencion_ct = ContentType.objects.get(app_label='doctor', model='atencion')
servicios_adicionales_ct = ContentType.objects.get(app_label='doctor', model='serviciosadicionales')
pago_ct = ContentType.objects.get(app_label='doctor', model='pago')


# Patient permissions.busca un objeto y, si no existe, lo crea automáticamente. Devueleve una tupla(objeto,encontrado).
patient_view_tupla = Permission.objects.get_or_create(codename='view_patient', name='Can view Paciente', content_type=patient_ct)
patient_view = Permission.objects.get_or_create(codename='view_patient', name='Can view Paciente', content_type=patient_ct)[0]
patient_add = Permission.objects.get_or_create(codename='add_patient', name='Can add Paciente', content_type=patient_ct)[0]
patient_change = Permission.objects.get_or_create(codename='change_patient', name='Can change Paciente', content_type=patient_ct)[0]
patient_delete = Permission.objects.get_or_create(codename='delete_patient', name='Can delete Paciente', content_type=patient_ct)[0]

# Diagnosis permissions
diagnosis_view = Permission.objects.get_or_create(codename='view_diagnosis', name='Can view Diagnóstico', content_type=diagnosis_ct)[0]
diagnosis_add = Permission.objects.get_or_create(codename='add_diagnosis', name='Can add Diagnóstico', content_type=diagnosis_ct)[0]
diagnosis_change = Permission.objects.get_or_create(codename='change_diagnosis', name='Can change Diagnóstico', content_type=diagnosis_ct)[0]
diagnosis_delete = Permission.objects.get_or_create(codename='delete_diagnosis', name='Can delete Diagnóstico', content_type=diagnosis_ct)[0]


# Doctor permissions
doctor_view = Permission.objects.get_or_create(codename='view_doctor', name='Can view Doctor', content_type=doctor_ct)[0]
doctor_add = Permission.objects.get_or_create(codename='add_doctor', name='Can add Doctor', content_type=doctor_ct)[0]
doctor_change = Permission.objects.get_or_create(codename='change_doctor', name='Can change Doctor', content_type=doctor_ct)[0]
doctor_delete = Permission.objects.get_or_create(codename='delete_doctor', name='Can delete Doctor', content_type=doctor_ct)[0]


# Empleados permissions
empleado_view = Permission.objects.get_or_create(codename='view_empleado', name='Can view Empleado', content_type=empleados_ct)[0]
empleado_add = Permission.objects.get_or_create(codename='add_empleado', name='Can add Empleado', content_type=empleados_ct)[0]
empleado_change = Permission.objects.get_or_create(codename='change_empleado', name='Can change Empleado', content_type=empleados_ct)[0]
empleado_delete = Permission.objects.get_or_create(codename='delete_empleado', name='Can delete Empleado', content_type=empleados_ct)[0]


# Medicamento permissions
medicamento_view = Permission.objects.get_or_create(codename='view_medicamento', name='Can view Medicamento', content_type=medicamento_ct)[0]
medicamento_add = Permission.objects.get_or_create(codename='add_medicamento', name='Can add Medicamento', content_type=medicamento_ct)[0]
medicamento_change = Permission.objects.get_or_create(codename='change_medicamento', name='Can change Medicamento', content_type=medicamento_ct)[0]
medicamento_delete = Permission.objects.get_or_create(codename='delete_medicamento', name='Can delete Medicamento', content_type=medicamento_ct)[0]


#  Gasto Mensual permissions
gasto_mensual_view = Permission.objects.get_or_create(codename='view_gastomensual', name='Can view Gasto Mensual', content_type=gasto_mensual_ct)[0]
gasto_mensual_add = Permission.objects.get_or_create(codename='add_gastomensual', name='Can add Gasto Mensual', content_type=gasto_mensual_ct)[0]
gasto_mensual_change = Permission.objects.get_or_create(codename='change_gastomensual', name='Can change Gasto Mensual', content_type=gasto_mensual_ct)[0]
gasto_mensual_delete = Permission.objects.get_or_create(codename='delete_gastomensual', name='Can delete Gasto Mensual', content_type=gasto_mensual_ct)[0]



#  Horario Atencion permissions
horario_atencion_view = Permission.objects.get_or_create(codename='view_horario_atencion', name='Can view Horario Atencion', content_type=horario_atencion_ct)[0]
horario_atencion_add = Permission.objects.get_or_create(codename='add_horario_atencion', name='Can add Horario Atencion', content_type=horario_atencion_ct)[0]
horario_atencion_change = Permission.objects.get_or_create(codename='change_horario_atencion', name='Can change Horario Atencion', content_type=horario_atencion_ct)[0]
horario_atencion_delete = Permission.objects.get_or_create(codename='delete_horario_atencion', name='Can delete Horario Atencion', content_type=horario_atencion_ct)[0]

#  Cita Medica permissions
cita_medica_view = Permission.objects.get_or_create(codename='view_cita_medica', name='Can view Cita Medica', content_type=cita_medica_ct)[0]
cita_medica_add = Permission.objects.get_or_create(codename='add_cita_medica', name='Can add Cita Medica', content_type=cita_medica_ct)[0]
cita_medica_change = Permission.objects.get_or_create(codename='change_cita_medica', name='Can change Cita Medica', content_type=cita_medica_ct)[0]
cita_medica_delete = Permission.objects.get_or_create(codename='delete_cita_medica', name='Can delete Cita Medica', content_type=cita_medica_ct)[0]




#  Atencion permissions
atencion_view = Permission.objects.get_or_create(codename='view_atencion_m', name='Can view atencion', content_type=atencion_ct)[0]
atencion_add = Permission.objects.get_or_create(codename='add_atencion_m', name='Can add atencion', content_type=atencion_ct)[0]
atencion_change = Permission.objects.get_or_create(codename='change_atencion_m', name='Can change atencion', content_type=atencion_ct)[0]
atencion_delete = Permission.objects.get_or_create(codename='delete_atencion_m', name='Can delete atencion', content_type=atencion_ct)[0]


#  Servicios Adicionales permissions
servicios_adicionales_view = Permission.objects.get_or_create(codename='view_servicios_adicionales', name='Can view Servicios Adicionales', content_type=servicios_adicionales_ct)[0]
servicios_adicionales_add = Permission.objects.get_or_create(codename='add_servicios_adicionales', name='Can add Servicios Adicionales', content_type=servicios_adicionales_ct)[0]
servicios_adicionales_change = Permission.objects.get_or_create(codename='change_servicios_adicionales', name='Can change Servicios Adicionales', content_type=servicios_adicionales_ct)[0]
servicios_adicionales_delete = Permission.objects.get_or_create(codename='delete_servicios_adicionales', name='Can delete Servicios Adicionales', content_type=servicios_adicionales_ct)[0]


#  Pago permissions
pago_view = Permission.objects.get_or_create(codename='view_pago', name='Can view Pago', content_type=pago_ct)[0]
pago_add = Permission.objects.get_or_create(codename='add_pago', name='Can add Pago', content_type=pago_ct)[0]
pago_change = Permission.objects.get_or_create(codename='change_pago', name='Can change Pago', content_type=pago_ct)[0]
pago_delete = Permission.objects.get_or_create(codename='delete_pago', name='Can delete Pago', content_type=pago_ct)[0]


# Add permissions to modules
module1.permissions.add(patient_view, patient_add, patient_change, patient_delete)
module2.permissions.add(diagnosis_view, diagnosis_add, diagnosis_change, diagnosis_delete)
module3.permissions.add(atencion_view, atencion_add, atencion_change, atencion_delete)
module4.permissions.add(horario_atencion_view, horario_atencion_add, horario_atencion_change, horario_atencion_delete)
module5.permissions.add(servicios_adicionales_view, servicios_adicionales_add, servicios_adicionales_change, servicios_adicionales_delete)
module6.permissions.add(cita_medica_view, cita_medica_add, cita_medica_change, cita_medica_delete)
module7.permissions.add(gasto_mensual_view, gasto_mensual_add, gasto_mensual_change, gasto_mensual_delete)
module8.permissions.add(medicamento_view, medicamento_add, medicamento_change, medicamento_delete)
module9.permissions.add(pago_view, pago_add, pago_change, pago_delete)
module10.permissions.add(doctor_view, doctor_add, doctor_change, doctor_delete)
module11.permissions.add(empleado_view, empleado_add, empleado_change, empleado_delete)



# Create GroupModulePermission records
# For Médicos with Patient module
gmp1 = GroupModulePermission.objects.create(group=group_medicos, module=module1)
gmp1.permissions.add(patient_view, patient_add, patient_change, patient_delete)

# For Médicos with Diagnosis module
gmp2 = GroupModulePermission.objects.create(group=group_medicos, module=module5)
gmp2.permissions.add(diagnosis_view, diagnosis_add, diagnosis_change)

# For Asistentes with Patient module (limited permissions)
gmp3 = GroupModulePermission.objects.create(group=group_asistentes, module=module1)
gmp3.permissions.add(patient_view, patient_add)

# For Asistentes with Diagnosis module (view only)
gmp4 = GroupModulePermission.objects.create(group=group_asistentes, module=module5)
gmp4.permissions.add(diagnosis_view)