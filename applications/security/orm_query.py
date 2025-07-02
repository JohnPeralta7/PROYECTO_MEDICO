#!/usr/bin/env python3
"""
Script para asignar permisos específicos por grupos en el sistema clínico.

Grupos y sus permisos:
- Asistente: Cita médica, Medicamentos, Pagos, Doctores, Empleados
- Médicos: Gasto mensual, Pacientes, Diagnóstico, Atención, Horario de atención, Servicios adicionales

Ejecutar con: python manage.py shell < applications/security/orm_query.py
"""

import os
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from applications.security.models import Module, GroupModulePermission
from applications.core.models import Paciente, Doctor, Empleado, Medicamento, Diagnostico, GastoMensual
from applications.doctor.models import CitaMedica, Atencion, HorarioAtencion, ServiciosAdicionales, Pago

def pausar_y_limpiar():
    input("Presione una tecla para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

print("=" * 80)
print("🏥 SCRIPT DE ASIGNACIÓN DE PERMISOS POR GRUPOS")
print("=" * 80)
print("\n📋 Configurando permisos para:")
print("   👥 Grupo Asistente: Cita médica, Medicamentos, Pagos, Doctores, Empleados")
print("   👨‍⚕️ Grupo Médicos: Gasto mensual, Pacientes, Diagnóstico, Atención, Horario de atención, Servicios adicionales")
print("\n")

# ==========================================
# 1. VERIFICAR Y CREAR GRUPOS
# ==========================================
print("1️⃣ Verificando y creando grupos...")

# Crear o obtener grupos
grupo_asistente, created_asistente = Group.objects.get_or_create(name="Asistente")
if created_asistente:
    print("   ✅ Grupo 'Asistente' creado")
else:
    print("   ℹ️ Grupo 'Asistente' ya existía")

grupo_medicos, created_medicos = Group.objects.get_or_create(name="Médicos")
if created_medicos:
    print("   ✅ Grupo 'Médicos' creado")
else:
    print("   ℹ️ Grupo 'Médicos' ya existía")

print(f"   📊 Grupo Asistente ID: {grupo_asistente.id}")
print(f"   📊 Grupo Médicos ID: {grupo_medicos.id}")
pausar_y_limpiar()

# ==========================================
# 2. OBTENER CONTENT TYPES Y PERMISOS
# ==========================================
print("2️⃣ Obteniendo Content Types y Permisos...")

# Diccionario para almacenar los content types
content_types = {}
permisos = {}

# Definir modelos y sus apps
modelos_info = {
    'cita_medica': ('doctor', 'citamedica'),
    'medicamento': ('core', 'medicamento'),
    'pago': ('doctor', 'pago'),
    'doctor': ('core', 'doctor'),
    'empleado': ('core', 'empleado'),
    'gasto_mensual': ('core', 'gastomensual'),
    'paciente': ('core', 'paciente'),
    'diagnostico': ('core', 'diagnostico'),
    'atencion': ('doctor', 'atencion'),
    'horario_atencion': ('doctor', 'horarioatencion'),
    'servicios_adicionales': ('doctor', 'serviciosadicionales'),
}

# Obtener content types
for modelo, (app, model_name) in modelos_info.items():
    try:
        ct = ContentType.objects.get(app_label=app, model=model_name)
        content_types[modelo] = ct
        print(f"   ✅ Content Type '{modelo}': {app}.{model_name}")
        
        # Obtener permisos para este content type
        permisos[modelo] = {
            'view': Permission.objects.get(content_type=ct, codename=f'view_{model_name}'),
            'add': Permission.objects.get(content_type=ct, codename=f'add_{model_name}'),
            'change': Permission.objects.get(content_type=ct, codename=f'change_{model_name}'),
            'delete': Permission.objects.get(content_type=ct, codename=f'delete_{model_name}'),
        }
        
    except ContentType.DoesNotExist:
        print(f"   ❌ Content Type '{modelo}' no encontrado: {app}.{model_name}")
    except Permission.DoesNotExist as e:
        print(f"   ⚠️ Algunos permisos para '{modelo}' no encontrados: {e}")

print(f"\n   📊 Total Content Types encontrados: {len(content_types)}")
print(f"   📊 Total grupos de permisos: {len(permisos)}")

pausar_y_limpiar()

# ==========================================
# 3. BUSCAR Y VERIFICAR MÓDULOS
# ==========================================
print("3️⃣ Buscando módulos en el sistema...")

# Definir los módulos que necesitamos encontrar
modulos_requeridos = {
    # Para Asistente
    'cita_medica': ['doctor/citas_list/', 'Cita Medica', 'doctor/cita_medica_list/'],
    'medicamento': ['core/medicamento_list/', 'Medicamento', 'core/medicamentos_list/'],
    'pago': ['doctor/pago_list/', 'Pago', 'doctor/pagos_list/'],
    'doctor': ['core/doctor_list/', 'Doctor', 'core/doctores_list/'],
    'empleado': ['core/empleado_list/', 'Empleado', 'core/empleados_list/'],
    
    # Para Médicos
    'gasto_mensual': ['core/gastos_mensual_list/', 'Gastos Mensual', 'core/gasto_mensual_list/'],
    'paciente': ['core/paciente_list/', 'Paciente', 'core/pacientes_list/'],
    'diagnostico': ['core/diagnostico_list/', 'Diagnostico', 'core/diagnosticos_list/'],
    'atencion': ['doctor/atencion_list/', 'Atencion', 'doctor/atenciones_list/'],
    'horario_atencion': ['doctor/horario_atencion_list/', 'Horario de Atencion'],
    'servicios_adicionales': ['doctor/servicio_adicional_list/', 'Servicios Adicionales', 'doctor/servicios_adicionales_list/'],
}

# Diccionario para almacenar los módulos encontrados
modulos_encontrados = {}

print("   🔍 Buscando módulos por URL y nombre...")
for clave, posibles_urls in modulos_requeridos.items():
    modulo_encontrado = None
    
    for url_o_nombre in posibles_urls:
        # Buscar por URL
        modulo = Module.objects.filter(url__icontains=url_o_nombre.replace('_list/', '')).first()
        if not modulo:
            # Buscar por nombre
            modulo = Module.objects.filter(name__icontains=url_o_nombre).first()
        
        if modulo:
            modulo_encontrado = modulo
            print(f"   ✅ Módulo '{clave}' encontrado: {modulo.name} ({modulo.url})")
            break
    
    if modulo_encontrado:
        modulos_encontrados[clave] = modulo_encontrado
    else:
        print(f"   ❌ Módulo '{clave}' NO encontrado. URLs buscadas: {posibles_urls}")

print(f"\n   📊 Módulos encontrados: {len(modulos_encontrados)} de {len(modulos_requeridos)}")

# Mostrar todos los módulos disponibles si faltan algunos
if len(modulos_encontrados) < len(modulos_requeridos):
    print("\n   📋 Todos los módulos disponibles en el sistema:")
    for modulo in Module.objects.all().order_by('menu__name', 'name'):
        print(f"      - {modulo.name} | URL: {modulo.url} | Menú: {modulo.menu.name}")

pausar_y_limpiar()

# ==========================================
# 4. ASIGNAR PERMISOS DE MODELOS A MÓDULOS
# ==========================================
print("4️⃣ Asignando permisos de modelos a módulos...")

# Mapear qué permisos corresponden a cada módulo
mapeo_permisos_modulos = {
    'cita_medica': 'cita_medica',
    'medicamento': 'medicamento', 
    'pago': 'pago',
    'doctor': 'doctor',
    'empleado': 'empleado',
    'gasto_mensual': 'gasto_mensual',
    'paciente': 'paciente',
    'diagnostico': 'diagnostico',
    'atencion': 'atencion',
    'horario_atencion': 'horario_atencion',
    'servicios_adicionales': 'servicios_adicionales',
}

print("   🔗 Asignando permisos a módulos...")
for modulo_clave, permisos_clave in mapeo_permisos_modulos.items():
    if modulo_clave in modulos_encontrados and permisos_clave in permisos:
        modulo = modulos_encontrados[modulo_clave]
        permisos_modelo = permisos[permisos_clave]
        
        # Limpiar permisos existentes
        modulo.permissions.clear()
        
        # Asignar todos los permisos del modelo al módulo
        modulo.permissions.add(
            permisos_modelo['view'],
            permisos_modelo['add'],
            permisos_modelo['change'],
            permisos_modelo['delete']
        )
        
        print(f"   ✅ Permisos asignados a módulo '{modulo.name}': view, add, change, delete")
    else:
        if modulo_clave not in modulos_encontrados:
            print(f"   ⚠️ Módulo '{modulo_clave}' no encontrado, saltando...")
        if permisos_clave not in permisos:
            print(f"   ⚠️ Permisos '{permisos_clave}' no encontrados, saltando...")

pausar_y_limpiar()

# ==========================================
# 5. CREAR GROUP MODULE PERMISSIONS PARA ASISTENTE
# ==========================================
print("5️⃣ Asignando permisos al grupo ASISTENTE...")

# Módulos para el grupo Asistente
modulos_asistente = ['cita_medica', 'medicamento', 'pago', 'doctor', 'empleado']

print(f"   👥 Configurando permisos para grupo: {grupo_asistente.name}")

for modulo_clave in modulos_asistente:
    if modulo_clave in modulos_encontrados and modulo_clave in permisos:
        modulo = modulos_encontrados[modulo_clave]
        permisos_modelo = permisos[modulo_clave]
        
        # Crear o actualizar GroupModulePermission
        gmp, created = GroupModulePermission.objects.get_or_create(
            group=grupo_asistente,
            module=modulo
        )
        
        # Limpiar permisos existentes
        gmp.permissions.clear()
        
        # Asignar permisos (Para asistente: view, add, change - no delete)
        gmp.permissions.add(
            permisos_modelo['view'],
            permisos_modelo['add'],
            permisos_modelo['change'],
            # No agregamos 'delete' para asistentes por seguridad
        )
        
        accion = "creado" if created else "actualizado"
        print(f"   ✅ GroupModulePermission {accion}: {grupo_asistente.name} -> {modulo.name}")
        print(f"      Permisos: view, add, change")
    else:
        print(f"   ⚠️ Saltando '{modulo_clave}' - módulo o permisos no encontrados")

pausar_y_limpiar()

# ==========================================
# 6. CREAR GROUP MODULE PERMISSIONS PARA MÉDICOS
# ==========================================
print("6️⃣ Asignando permisos al grupo MÉDICOS...")

# Módulos para el grupo Médicos
modulos_medicos = ['gasto_mensual', 'paciente', 'diagnostico', 'atencion', 'horario_atencion', 'servicios_adicionales']

print(f"   👨‍⚕️ Configurando permisos para grupo: {grupo_medicos.name}")

for modulo_clave in modulos_medicos:
    if modulo_clave in modulos_encontrados and modulo_clave in permisos:
        modulo = modulos_encontrados[modulo_clave]
        permisos_modelo = permisos[modulo_clave]
        
        # Crear o actualizar GroupModulePermission
        gmp, created = GroupModulePermission.objects.get_or_create(
            group=grupo_medicos,
            module=modulo
        )
        
        # Limpiar permisos existentes
        gmp.permissions.clear()
        
        # Asignar todos los permisos para médicos
        gmp.permissions.add(
            permisos_modelo['view'],
            permisos_modelo['add'],
            permisos_modelo['change'],
            permisos_modelo['delete'],
        )
        
        accion = "creado" if created else "actualizado"
        print(f"   ✅ GroupModulePermission {accion}: {grupo_medicos.name} -> {modulo.name}")
        print(f"      Permisos: view, add, change, delete")
    else:
        print(f"   ⚠️ Saltando '{modulo_clave}' - módulo o permisos no encontrados")

pausar_y_limpiar()

# ==========================================
# 7. VERIFICACIÓN FINAL
# ==========================================
print("7️⃣ Verificación final de permisos asignados...")

print("\n📊 RESUMEN DE PERMISOS ASIGNADOS:")

print(f"\n👥 Grupo: {grupo_asistente.name}")
asistente_permisos = GroupModulePermission.objects.filter(group=grupo_asistente)
print(f"   Total de módulos asignados: {asistente_permisos.count()}")
for gmp in asistente_permisos:
    permisos_nombres = [p.codename for p in gmp.permissions.all()]
    print(f"   📁 {gmp.module.name}: {', '.join(permisos_nombres)}")

print(f"\n👨‍⚕️ Grupo: {grupo_medicos.name}")
medicos_permisos = GroupModulePermission.objects.filter(group=grupo_medicos)
print(f"   Total de módulos asignados: {medicos_permisos.count()}")
for gmp in medicos_permisos:
    permisos_nombres = [p.codename for p in gmp.permissions.all()]
    print(f"   📁 {gmp.module.name}: {', '.join(permisos_nombres)}")

# ==========================================
# 8. VERIFICAR EN BASE DE DATOS
# ==========================================
print("\n8️⃣ Verificación en base de datos...")

print("\n🔍 Consulta directa a GroupModulePermission:")
print("SELECT statement: GroupModulePermission.objects.all()")

todos_gmp = GroupModulePermission.objects.select_related('group', 'module').prefetch_related('permissions')
print(f"Total de registros: {todos_gmp.count()}")

for gmp in todos_gmp:
    print(f"Grupo: {gmp.group.name} | Módulo: {gmp.module.name} | Permisos: {gmp.permissions.count()}")

print("\n" + "=" * 80)
print("✅ SCRIPT COMPLETADO EXITOSAMENTE")
print("=" * 80)
print("\n📋 Resumen de acciones realizadas:")
print("   ✅ Grupos verificados/creados: Asistente, Médicos")
print("   ✅ Content Types y permisos obtenidos para todos los modelos")
print("   ✅ Módulos del sistema identificados")
print("   ✅ Permisos asignados a módulos correspondientes")
print("   ✅ GroupModulePermissions creados para ambos grupos")
print("\n🎯 Los grupos ahora deberían aparecer con permisos en la interfaz web")
print("🔄 Recarga la página de gestión de permisos para ver los cambios")

print("\n💡 Si algún módulo no apareció, revisa:")
print("   - Que los módulos estén creados en la base de datos")
print("   - Que las URLs coincidan con las definidas en urls.py")
print("   - Que los permisos del modelo estén creados correctamente")

print("\n🚀 Para ejecutar este script:")
print("   python manage.py shell < applications/security/orm_query.py")

pausar_y_limpiar()