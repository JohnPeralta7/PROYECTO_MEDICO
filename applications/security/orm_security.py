from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from applications.security.models import GroupModulePermission, Menu, Module, User

# Verificar si ya existe el menú de Seguridad
menu_security, created = Menu.objects.get_or_create(
    name='Seguridad',
    defaults={
        'icon': 'fa fa-shield-alt',
        'order': 1
    }
)

if created:
    print("Menú de Seguridad creado")
else:
    print("Menú de Seguridad ya existía, usando el existente")

# Verificar módulos existentes para no duplicar
existing_modules = {
    module.url: module 
    for module in Module.objects.filter(menu=menu_security)
}

# Lista para los nuevos módulos que serán creados
new_modules = []

# Definiciones de módulos
module_definitions = [
    {
        'url': 'security/menu_list/', 
        'name': 'Gestión de Menús', 
        'description': 'Administrar los menús del sistema', 
        'icon': 'fa fa-list', 
        'order': 1
    },
    {
        'url': 'security/module_list/', 
        'name': 'Gestión de Módulos', 
        'description': 'Administrar los módulos del sistema', 
        'icon': 'fa fa-th-large', 
        'order': 2
    },
    {
        'url': 'security/user_list/', 
        'name': 'Gestión de Usuarios', 
        'description': 'Administrar los usuarios del sistema', 
        'icon': 'fa fa-users', 
        'order': 3
    },
    {
        'url': 'security/group_module_permission_list/', 
        'name': 'Permisos por Módulo', 
        'description': 'Asignar permisos específicos a grupos por cada módulo', 
        'icon': 'fa fa-shield-alt', 
        'order': 4
    }
]

# Crear o actualizar módulos
created_security_modules = []
for module_def in module_definitions:
    if module_def['url'] in existing_modules:
        # Usar módulo existente
        module = existing_modules[module_def['url']]
        print(f"Módulo {module_def['name']} ya existía, usando el existente")
        created_security_modules.append(module)
    else:
        # Crear nuevo módulo
        module = Module(menu=menu_security, **module_def)
        new_modules.append(module)

# Crear módulos que no existen
if new_modules:
    batch_created_modules = Module.objects.bulk_create(new_modules)
    created_security_modules.extend(batch_created_modules)
    print(f"Creados {len(batch_created_modules)} nuevos módulos")

# Asegurarnos que tenemos los 5 módulos
module_menu = next((m for m in created_security_modules if m.url == 'security/menu_list/'), None)
module_modules = next((m for m in created_security_modules if m.url == 'security/module_list/'), None)
module_users = next((m for m in created_security_modules if m.url == 'security/user_list/'), None)
module_group_perms = next((m for m in created_security_modules if m.url == 'security/group_module_permission_list/'), None)

# Obtener ContentTypes para menu y module
menu_ct = ContentType.objects.get(app_label='security', model='menu')
module_ct = ContentType.objects.get(app_label='security', model='module')
group_module_permission_ct = ContentType.objects.get(app_label='security', model='groupmodulepermission')
user_ct = ContentType.objects.get(app_label='security', model='user')

# Obtener ContentTypes para patient y diagnosis si existen
try:
    patient_ct = ContentType.objects.get(app_label='core', model='paciente')
    diagnosis_ct = ContentType.objects.get(app_label='core', model='diagnostico')
    has_medical_models = True
except ContentType.DoesNotExist:
    has_medical_models = False
    print("Aviso: No se encontraron los modelos de pacientes o diagnósticos")

# Obtener o crear permisos para menu (correctamente)
menu_view, _ = Permission.objects.get_or_create(
    content_type=menu_ct, codename='view_menu', 
    defaults={'name': 'Can view Menu'}
)
menu_add, _ = Permission.objects.get_or_create(
    content_type=menu_ct, codename='add_menu', 
    defaults={'name': 'Can add Menu'}
)
menu_change, _ = Permission.objects.get_or_create(
    content_type=menu_ct, codename='change_menu', 
    defaults={'name': 'Can change Menu'}
)
menu_delete, _ = Permission.objects.get_or_create(
    content_type=menu_ct, codename='delete_menu', 
    defaults={'name': 'Can delete Menu'}
)

# Obtener o crear permisos para module (correctamente)
module_view, _ = Permission.objects.get_or_create(
    content_type=module_ct, codename='view_module', 
    defaults={'name': 'Can view Module'}
)
module_add, _ = Permission.objects.get_or_create(
    content_type=module_ct, codename='add_module', 
    defaults={'name': 'Can add Module'}
)
module_change, _ = Permission.objects.get_or_create(
    content_type=module_ct, codename='change_module', 
    defaults={'name': 'Can change Module'}
)
module_delete, _ = Permission.objects.get_or_create(
    content_type=module_ct, codename='delete_module', 
    defaults={'name': 'Can delete Module'}
)

# Obtener o crear permisos para group_module_permission
gmp_view, _ = Permission.objects.get_or_create(
    content_type=group_module_permission_ct, codename='view_groupmodulepermission', 
    defaults={'name': 'Can view Grupo Módulo Permiso'}
)
gmp_add, _ = Permission.objects.get_or_create(
    content_type=group_module_permission_ct, codename='add_groupmodulepermission', 
    defaults={'name': 'Can add Grupo Módulo Permiso'}
)
gmp_change, _ = Permission.objects.get_or_create(
    content_type=group_module_permission_ct, codename='change_groupmodulepermission', 
    defaults={'name': 'Can change Grupo Módulo Permiso'}
)
gmp_delete, _ = Permission.objects.get_or_create(
    content_type=group_module_permission_ct, codename='delete_groupmodulepermission', 
    defaults={'name': 'Can delete Grupo Módulo Permiso'}
)

# Obtener o crear permisos para user
user_view, _ = Permission.objects.get_or_create(
    content_type=user_ct, codename='view_user', 
    defaults={'name': 'Can view User'}
)
user_add, _ = Permission.objects.get_or_create(
    content_type=user_ct, codename='add_user', 
    defaults={'name': 'Can add User'}
)
user_change, _ = Permission.objects.get_or_create(
    content_type=user_ct, codename='change_user', 
    defaults={'name': 'Can change User'}
)
user_delete, _ = Permission.objects.get_or_create(
    content_type=user_ct, codename='delete_user', 
    defaults={'name': 'Can delete User'}
)


# Obtener permisos para pacientes y diagnósticos si existen
if has_medical_models:
    # Patient permissions
    patient_view, _ = Permission.objects.get_or_create(
        content_type=patient_ct, codename='view_patient',
        defaults={'name': 'Can view Paciente'}
    )
    patient_add, _ = Permission.objects.get_or_create(
        content_type=patient_ct, codename='add_patient',
        defaults={'name': 'Can add Paciente'}
    )
    patient_change, _ = Permission.objects.get_or_create(
        content_type=patient_ct, codename='change_patient',
        defaults={'name': 'Can change Paciente'}
    )
    patient_delete, _ = Permission.objects.get_or_create(
        content_type=patient_ct, codename='delete_patient',
        defaults={'name': 'Can delete Paciente'}
    )
    
    # Diagnosis permissions
    diagnosis_view, _ = Permission.objects.get_or_create(
        content_type=diagnosis_ct, codename='view_diagnosis',
        defaults={'name': 'Can view Diagnóstico'}
    )
    diagnosis_add, _ = Permission.objects.get_or_create(
        content_type=diagnosis_ct, codename='add_diagnosis',
        defaults={'name': 'Can add Diagnóstico'}
    )
    diagnosis_change, _ = Permission.objects.get_or_create(
        content_type=diagnosis_ct, codename='change_diagnosis',
        defaults={'name': 'Can change Diagnóstico'}
    )
    diagnosis_delete, _ = Permission.objects.get_or_create(
        content_type=diagnosis_ct, codename='delete_diagnosis',
        defaults={'name': 'Can delete Diagnóstico'}
    )

# Asignar permisos a módulos (si existen)
if module_menu:
    module_menu.permissions.clear()  # Limpiar permisos existentes
    module_menu.permissions.add(menu_view, menu_add, menu_change, menu_delete)
    print("Permisos asignados al módulo de Menús")

if module_modules:
    module_modules.permissions.clear()  # Limpiar permisos existentes
    module_modules.permissions.add(module_view, module_add, module_change, module_delete)
    print("Permisos asignados al módulo de Módulos")

if module_group_perms:
    module_group_perms.permissions.clear()  # Limpiar permisos existentes
    module_group_perms.permissions.add(gmp_view, gmp_add, gmp_change, gmp_delete)
    print("Permisos asignados al módulo de Permisos por Módulo")

# Asignar permisos al módulo de usuarios
if module_users:
    module_users.permissions.clear()  # Limpiar permisos existentes
    module_users.permissions.add(user_view, user_add, user_change, user_delete)
    print("Permisos asignados al módulo de Usuarios")


# Crear grupo de administradores si no existe
group_admin, created_group = Group.objects.get_or_create(name='Administradores')
if created_group:
    print("Grupo Administradores creado")
else:
    print("Grupo Administradores ya existía")

# Verificar si ya existen GroupModulePermission para evitar duplicados
if module_menu:
    gmp_admin_menu, created = GroupModulePermission.objects.get_or_create(
        group=group_admin, module=module_menu
    )
    gmp_admin_menu.permissions.clear()
    gmp_admin_menu.permissions.add(menu_view, menu_add, menu_change, menu_delete)
    print("Permisos de menú asignados al grupo Administradores")

if module_modules:
    gmp_admin_module, created = GroupModulePermission.objects.get_or_create(
        group=group_admin, module=module_modules
    )
    gmp_admin_module.permissions.clear()
    gmp_admin_module.permissions.add(module_view, module_add, module_change, module_delete)
    print("Permisos de módulo asignados al grupo Administradores")

if module_group_perms:
    gmp_admin_group_perms, created = GroupModulePermission.objects.get_or_create(
        group=group_admin, module=module_group_perms
    )
    gmp_admin_group_perms.permissions.clear()
    gmp_admin_group_perms.permissions.add(gmp_view, gmp_add, gmp_change, gmp_delete)
    print("Permisos de gestión de permisos por módulo asignados al grupo Administradores")

# Asignar permisos de usuario al grupo Administradores
if module_users:
    gmp_admin_users, created = GroupModulePermission.objects.get_or_create(
        group=group_admin, module=module_users
    )
    gmp_admin_users.permissions.clear()
    gmp_admin_users.permissions.add(user_view, user_add, user_change, user_delete)
    print("Permisos de gestión de usuarios asignados al grupo Administradores")


# NUEVO: Asignar permisos a todos los demás módulos
print("\nAsignando permisos de administrador a todos los módulos del sistema...")
all_modules = Module.objects.all()
modules_count = 0

for module in all_modules:
    # No reprocesar los módulos que ya manejamos
    if module in [module_menu, module_modules, module_users, module_group_perms]:
        continue
        
    gmp_admin_all, created = GroupModulePermission.objects.get_or_create(
        group=group_admin, module=module
    )
    
    # Obtener todos los permisos asociados a este módulo
    module_permissions = module.permissions.all()
    
    if not module_permissions:
        print(f"⚠️ El módulo '{module.name}' no tiene permisos asignados")
        continue
        
    # Asignar todos los permisos del módulo al grupo de administradores
    gmp_admin_all.permissions.clear()
    gmp_admin_all.permissions.add(*module_permissions)
    modules_count += 1
    
print(f"✅ Permisos actualizados para {modules_count} módulos adicionales")

# NUEVO: Asignar permisos de modelos médicos al grupo admin (si existen)
if has_medical_models:
    # Asignar permisos directos al grupo
    patient_permissions = [patient_view, patient_add, patient_change, patient_delete]
    diagnosis_permissions = [diagnosis_view, diagnosis_add, diagnosis_change, diagnosis_delete]
    
    # Asignar permisos de pacientes
    group_admin.permissions.add(*patient_permissions)
    
    # Asignar permisos de diagnósticos
    group_admin.permissions.add(*diagnosis_permissions)
    
    print("✅ Permisos de pacientes y diagnósticos asignados al grupo Administradores")

# Buscar usuario existente o crear uno nuevo
try:
    admin_user = User.objects.get(username='admin')
    admin_user.groups.add(group_admin)
    print("Usuario 'admin' añadido al grupo Administradores")
except User.DoesNotExist:
    # Crear usuario admin si no existe
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@sistema.com',
        password='1234',
        first_name='Administrador',
        last_name='Sistema',
        dni='9999999999',
        direction='Sistema',
        phone='9999999999',
        is_staff=True
    )
    admin_user.groups.add(group_admin)
    print("Usuario 'admin' creado y añadido al grupo Administradores")

print("\n======== CONFIGURACIÓN COMPLETADA ========")
print("✅ Menú de seguridad y módulos creados exitosamente!")
print("✅ Grupo Administradores ahora tiene acceso a TODOS los módulos del sistema")
print("✅ Se han asignado permisos específicos a los módulos de:")
print("   - Gestión de Menús")
print("   - Gestión de Módulos")
print("   - Gestión de Usuarios")
print("   - Gestión de Grupos")
print("   - Gestión de Permisos por Módulo")

print("\nPuedes acceder al sistema usando:")
print("- URL de menús: /security/menu_list/")
print("- URL de módulos: /security/module_list/")
print("- URL de usuarios: /security/user_list/")
print("- URL de grupos: /security/group_list/")
print("- URL de gestión de permisos por módulo: /security/group_module_permission_list/")

print("\nSi algún módulo no está visible, ejecuta este script nuevamente")
print("o verifica los permisos asignados al grupo Administradores.")