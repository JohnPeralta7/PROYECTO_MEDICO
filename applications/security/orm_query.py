<<<<<<< HEAD
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
=======
import os
from applications.security.models import Menu
from django.db.models import Q, Count, Max, Min, Avg
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6

def pausar_y_limpiar():
    input("Presione una tecla para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

<<<<<<< HEAD
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
=======
# Consulta 1: Obtener todos los menús: devuelve un queryset: lista de objetos Menu
print("Sentencia: Menu.objects.all()")
todos_los_menus = Menu.objects.all().order_by('id')
print("Resultado:", todos_los_menus)
pausar_y_limpiar()

# Consulta 2: Usando filter sin condiciones
print("Sentencia: Menu.objects.filter()")
todos_los_menus = Menu.objects.filter()
print("Resultado:", todos_los_menus)
pausar_y_limpiar()

# Consulta 3: Usando values para obtener diccionarios
print("Sentencia: Menu.objects.values('id', 'name', 'icon', 'order')")
menus_valores = Menu.objects.values('id', 'name', 'icon', 'order')
print("Resultado (QuerySet):", menus_valores)
menus_valores_lista = list(menus_valores)
print("Resultado como lista de diccionarios:", menus_valores_lista)
pausar_y_limpiar()

#Consulta 4: Usando values_list para obtener tuplas
print("Sentencia: Menu.objects.values_list('id', 'name', 'icon', 'order')")
menus_valores_tuplas = Menu.objects.values_list('id', 'name', 'icon', 'order')
print("Resultado (QuerySet):", menus_valores_tuplas)
menus_valores_tuplas_lista = list(menus_valores_tuplas)
print("Resultado como lista de tuplas:", menus_valores_tuplas_lista)
pausar_y_limpiar()

# Consulta 5: Usando values_list con flat=True
print("Sentencia: Menu.objects.values_list('name', flat=True)")
nombres_menus = Menu.objects.values_list('name', flat=True)
print("Resultado (QuerySet):", nombres_menus)
nombres_menus_lista = list(nombres_menus)
print("Resultado como lista de nombres:", nombres_menus_lista)
pausar_y_limpiar()

# Consulta 6: Convertir QuerySet a lista
print("Sentencia: list(Menu.objects.all())")
menus_lista = list(Menu.objects.all())
print("Resultado:", menus_lista)
pausar_y_limpiar()

print("Sentencia: Recorrido de list(Menu.objects.all())")
print(""" for menu in menus_lista:  print(menu.id, menu.name)""")
# recorrido de la lista
for menu in menus_lista:
    print(menu.id, menu.name)
pausar_y_limpiar()

# Consulta 7: Obtener menú por ID
print("Sentencia: Menu.objects.get(id=1)")
menu = Menu.objects.get(id=1)
print("Resultado:", menu)
pausar_y_limpiar()

# Consulta 8: Obtener menú por nombre
print("Sentencia: Menu.objects.get(name='Admin')")
menu = Menu.objects.get(name='Consultas')
print("Resultado:", menu)
pausar_y_limpiar()

# Consulta 9: Filtrar por icono
print("Sentencia: Menu.objects.filter(icon='bi bi-calendar-x-fill')")
menus_filtrados = Menu.objects.filter(icon='bi bi-calendar-x-fill')
print("Resultado:", menus_filtrados)
pausar_y_limpiar()

# Consulta 10: Excluir por icono
print("Sentencia: Menu.objects.exclude(icon='bi bi-calendar-x-fill')")
menus_excluidos = Menu.objects.exclude(icon='bi bi-calendar-x-fill')
print("Resultado:", menus_excluidos)
pausar_y_limpiar()

# Consulta 11: Obtener primer menú
print("Sentencia: Menu.objects.first()")
primer_menu = Menu.objects.first()
print("Resultado:", primer_menu)
pausar_y_limpiar()

# Consulta 12: Obtener último menú
print("Sentencia: Menu.objects.last()")
ultimo_menu = Menu.objects.last()
print("Resultado:", ultimo_menu)
pausar_y_limpiar()

# Consulta 13: Verificar si existen menús
print("Sentencia: Menu.objects.exists()")
tiene_menus = Menu.objects.exists()
print("Resultado:", tiene_menus)
pausar_y_limpiar()

# Consulta 14: Ordenar por campo
print("Sentencia: Menu.objects.order_by('order')")
menus_ordenados = Menu.objects.order_by('order')
print("Resultado:", menus_ordenados)
pausar_y_limpiar()

# Consulta 15: Ordenar descendente
print("Sentencia: Menu.objects.order_by('-order')")
menus_ordenados_desc = Menu.objects.order_by('-order')
print("Resultado:", menus_ordenados_desc)
pausar_y_limpiar()

# Consulta 16: Ordenar por múltiples campos
print("Sentencia: Menu.objects.order_by('order', 'name')")
menus_orden_multiple = Menu.objects.order_by('order', 'name')
print("Resultado:", menus_orden_multiple)
pausar_y_limpiar()

# Consulta 17: Búsqueda que contiene (case sensitive)
print("Sentencia: Menu.objects.filter(name__contains='admin')")
menus_contiene = Menu.objects.filter(name__icontains='admin')
print("Resultado:", menus_contiene)
pausar_y_limpiar()

# Consulta 18: Búsqueda que contiene (case insensitive)
print("Sentencia: Menu.objects.filter(name__icontains='admin')")
menus_icontiene = Menu.objects.filter(name__icontains='admin')
print("Resultado:", menus_icontiene)
pausar_y_limpiar()

# Consulta 19: Comienza con
print("Sentencia: Menu.objects.filter(name__startswith='A')")
menus_comienza = Menu.objects.filter(name__startswith='A')
print("Resultado:", menus_comienza)
pausar_y_limpiar()

# Consulta 20: Termina con
print("Sentencia: Menu.objects.filter(name__endswith='n')")
menus_termina = Menu.objects.filter(name__endswith='n')
print("Resultado:", menus_termina)
pausar_y_limpiar()

# Consulta 21: Mayor que
print("Sentencia: Menu.objects.filter(order__gt=5)")
menus_mayor = Menu.objects.filter(order__gt=5)
print("Resultado:", menus_mayor)
pausar_y_limpiar()

# Consulta 22: Menor que
print("Sentencia: Menu.objects.filter(order__lt=5)")
menus_menor = Menu.objects.filter(order__lt=5)
print("Resultado:", menus_menor)
pausar_y_limpiar()

# Consulta 23: En una lista
print("Sentencia: Menu.objects.filter(name__in=['Admin', 'Usuario', 'Reportes'])")
menus_en_lista = Menu.objects.filter(name__in=['Admin', 'Usuario', 'Reportes'])
print("Resultado:", menus_en_lista)
pausar_y_limpiar()

# Consulta 24: En un rango
print("Sentencia: Menu.objects.filter(order__range=(1, 5))")
menus_rango = Menu.objects.filter(order__range=(1, 5))
print("Resultado:", menus_rango)
pausar_y_limpiar()

# Consulta 25: Condición OR
print("Sentencia: Menu.objects.filter(Q(name='Admin') | Q(name='Usuario'))")
menus_or = Menu.objects.filter(Q(name='Admin') | Q(name='Usuario'))
print("Resultado:", menus_or)
pausar_y_limpiar()

# Consulta 26: Condición AND
print("Sentencia: Menu.objects.filter(Q(name='Admin') & Q(order__gt=5))")
menus_and = Menu.objects.filter(Q(name='Admin') & Q(order__gt=5))
print("Resultado:", menus_and)
pausar_y_limpiar()

# Consulta 27: Condición NOT
print("Sentencia: Menu.objects.filter(~Q(name='Admin'))")
menus_not = Menu.objects.filter(~Q(name='Admin'))
print("Resultado:", menus_not)
pausar_y_limpiar()

# Consulta 28: Contar
print("Sentencia: Menu.objects.count()")
cantidad_menus = Menu.objects.count()
print("Resultado:", cantidad_menus)
pausar_y_limpiar()

# Consulta 29: Valor máximo
print("Sentencia: Menu.objects.aggregate(Max('order'))")
orden_maximo = Menu.objects.aggregate(Max('order'))
print("Resultado:", orden_maximo)
pausar_y_limpiar()

# Consulta 30: Valor mínimo
print("Sentencia: Menu.objects.aggregate(Min('order'))")
orden_minimo = Menu.objects.aggregate(Min('order'))
print("Resultado:", orden_minimo)
pausar_y_limpiar()

# Consulta 31: Promedio
print("Sentencia: Menu.objects.aggregate(Avg('order'))")
orden_promedio = Menu.objects.aggregate(Avg('order'))
print("Resultado:", orden_promedio)
pausar_y_limpiar()

# Consulta 32: Primeros 5 menús
print("Sentencia: Menu.objects.all()[:5]")
menus_limitados = Menu.objects.all()[:5]
print("Resultado:", menus_limitados)
pausar_y_limpiar()

# Consulta 33: Menús del 5 al 10
print("Sentencia: Menu.objects.all()[5:10]")
menus_segmento = Menu.objects.all()[5:10]
print("Resultado:", menus_segmento)
pausar_y_limpiar()
""" Module.objects.filter( Q(url__icontains="security") & Q(id__lt=9) )
Out[42]: SELECT "security_module"."id",
       "security_module"."url",
       "security_module"."name",
       "security_module"."menu_id",
       "security_module"."description",
       "security_module"."icon",
       "security_module"."is_active",
       "security_module"."order"
  FROM "security_module"
 INNER JOIN "security_menu"
    ON ("security_module"."menu_id" = "security_menu"."id")
 WHERE (UPPER("security_module"."url"::text) LIKE UPPER('%security%') AND "security_module"."id" < 9)     
 ORDER BY "security_menu"."order" ASC,
          "security_menu"."name" ASC,
          "security_module"."order" ASC,
          "security_module"."name" ASC
 LIMIT 21 """
>>>>>>> c8f22bc0467a96966b05af9ed354b5f1d6c751b6
