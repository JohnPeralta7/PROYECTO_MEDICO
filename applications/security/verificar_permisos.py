#!/usr/bin/env python3
"""
Script simple para verificar los registros en la base de datos
Ejecutar con: python manage.py shell < applications/security/verificar_permisos.py
"""

from django.contrib.auth.models import Group, Permission
from applications.security.models import GroupModulePermission, Module

print("=" * 60)
print("🔍 VERIFICACIÓN DE REGISTROS EN BASE DE DATOS")
print("=" * 60)

# 1. Verificar grupos
print("\n1️⃣ GRUPOS EXISTENTES:")
grupos = Group.objects.all()
print(f"Total de grupos: {grupos.count()}")
for grupo in grupos:
    print(f"  • {grupo.name} (ID: {grupo.id})")

# 2. Verificar GroupModulePermission
print("\n2️⃣ GROUP MODULE PERMISSIONS:")
gmps = GroupModulePermission.objects.all()
print(f"Total de GroupModulePermissions: {gmps.count()}")

if gmps.count() > 0:
    for gmp in gmps:
        print(f"  • Grupo: {gmp.group.name} -> Módulo: {gmp.module.name}")
        print(f"    Permisos ({gmp.permissions.count()}): {[p.codename for p in gmp.permissions.all()]}")
else:
    print("  ❌ NO HAY registros de GroupModulePermission")

# 3. Verificar módulos
print("\n3️⃣ MÓDULOS DISPONIBLES:")
modulos = Module.objects.all()
print(f"Total de módulos: {modulos.count()}")
for modulo in modulos[:10]:  # Solo mostrar primeros 10
    print(f"  • {modulo.name} ({modulo.url}) - Permisos: {modulo.permissions.count()}")

# 4. Buscar específicamente los grupos que nos interesan
print("\n4️⃣ BÚSQUEDA ESPECÍFICA:")
try:
    asistente = Group.objects.get(name="Asistente")
    print(f"✅ Grupo 'Asistente' encontrado (ID: {asistente.id})")
    
    asistente_permisos = GroupModulePermission.objects.filter(group=asistente)
    print(f"   Permisos asignados: {asistente_permisos.count()}")
    for gmp in asistente_permisos:
        print(f"     - {gmp.module.name}")
        
except Group.DoesNotExist:
    print("❌ Grupo 'Asistente' NO encontrado")

try:
    medicos = Group.objects.get(name="Médicos")
    print(f"✅ Grupo 'Médicos' encontrado (ID: {medicos.id})")
    
    medicos_permisos = GroupModulePermission.objects.filter(group=medicos)
    print(f"   Permisos asignados: {medicos_permisos.count()}")
    for gmp in medicos_permisos:
        print(f"     - {gmp.module.name}")
        
except Group.DoesNotExist:
    print("❌ Grupo 'Médicos' NO encontrado")

# 5. Verificar si hay registros con nombres similares
print("\n5️⃣ BÚSQUEDA POR NOMBRES SIMILARES:")
grupos_similares = Group.objects.filter(name__icontains="asistente")
if grupos_similares.exists():
    print("Grupos que contienen 'asistente':")
    for g in grupos_similares:
        print(f"  • '{g.name}' (ID: {g.id})")
else:
    print("No se encontraron grupos con 'asistente'")

grupos_similares = Group.objects.filter(name__icontains="medic")
if grupos_similares.exists():
    print("Grupos que contienen 'medic':")
    for g in grupos_similares:
        print(f"  • '{g.name}' (ID: {g.id})")
else:
    print("No se encontraron grupos con 'medic'")

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 60)
